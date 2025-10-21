from pydantic import BaseModel
from typing import Optional, List
import os
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, JsonCssExtractionStrategy, CacheMode, LLMExtractionStrategy
from openai import AsyncOpenAI
import logging
import difflib
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import time
import json
from dotenv import load_dotenv
from pathlib import Path

# Load OPENAI_API_KEY from .env
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI API key if available
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Make it optional for basic functionality
# if not OPENAI_API_KEY:
#     raise RuntimeError('OPENAI_API_KEY not set in .env')

LLM_CACHE_DIR = Path(__file__).resolve().parent.parent.parent / 'llm_cache'
LLM_CACHE_TTL = 3600  # 1 hour
DEV_LLM_STUB = False  # Set True for dev stub mode
OPENAI_API_KEY_FALLBACK = None  # Fallback for OpenAI API key
GEMINI_API_KEY = None  # Fallback for Gemini API key
# Ensure cache dir exists
try:
    LLM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass


def _llm_cache_key(prompt: str) -> str:
    # simple hash key for prompt
    import hashlib

    h = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
    return h


def _llm_cache_get(prompt: str) -> Optional[str]:
    key = _llm_cache_key(prompt)
    p = LLM_CACHE_DIR / f"{key}.json"
    try:
        if not p.exists():
            logging.getLogger(__name__).debug("LLM cache miss (no file): %s", key)
            return None
        data = json.loads(p.read_text(encoding='utf-8'))
        ts = data.get('_ts', 0)
        if time.time() - ts > LLM_CACHE_TTL:
            try:
                p.unlink()
            except Exception:
                pass
            logging.getLogger(__name__).debug("LLM cache expired: %s", key)
            return None
        logging.getLogger(__name__).debug("LLM cache hit: %s", key)
        return data.get('resp')
    except Exception:
        logging.getLogger(__name__).exception("LLM cache read error: %s", p)
        return None


def _llm_cache_set(prompt: str, resp_text: str) -> None:
    key = _llm_cache_key(prompt)
    p = LLM_CACHE_DIR / f"{key}.json"
    try:
        payload = {'_ts': int(time.time()), 'resp': resp_text}
        p.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        logging.getLogger(__name__).debug("LLM cache write: %s (bytes=%d)", key, len(resp_text or ""))
    except Exception:
        logging.getLogger(__name__).exception("Failed to write LLM cache: %s", p)
if not OPENAI_API_KEY:
    raise RuntimeError('OPENAI_API_KEY not set in .env')

# NOTE: we avoid creating AsyncOpenAI at import time to prevent asyncio lifecycle issues.
# A client will be created lazily inside the relevance function.



class Product(BaseModel):
    product_name: str
    price: float
    rating: Optional[float] = None
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    retailer: Optional[str] = None
    final_score: Optional[float] = None
    recommendation: Optional[str] = None
    discount: Optional[str] = None  # e.g. '20% off', '₹500 off', etc.

class PlatformProducts(BaseModel):
    platform: str
    products: List[Product]
    price_low: Optional[float] = None
    price_avg: Optional[float] = None
    price_high: Optional[float] = None


class SearchResponse(BaseModel):
    amazon: PlatformProducts
    flipkart: PlatformProducts
    price_low: Optional[float] = None
    price_avg: Optional[float] = None
    price_high: Optional[float] = None
    ai_recommendation: Optional[str] = None


from .product_filter import filter_relevant_products

def _calculate_recommendation(products: List[Product], search_query: str) -> List[Product]:
    """Apply filtering and then a 70/30 heuristic: price (70%), rating (30%).
    
    Only considers products with:
    - Rating > 3.5 (must have a rating)
    - Price within reasonable range (not outliers)
    """
    if not products:
        return []
        
    # First filter out irrelevant products
    relevant_products = filter_relevant_products(products, search_query)
    
    # Filter out products without ratings or with ratings <= 3.5
    rated_products = [
        p for p in relevant_products 
        if p.rating is not None and p.rating > 3.5
    ]
    
    if not rated_products:
        # If no products meet the rating criteria, return empty list
        logging.getLogger(__name__).warning(
            "No products with rating > 3.5 found for query: %s", search_query
        )
        return []
    
    # Calculate price statistics to filter outliers
    prices = [p.price for p in rated_products if p.price is not None and p.price > 0]
    if not prices:
        return rated_products

    # Calculate median and interquartile range to identify reasonable prices
    sorted_prices = sorted(prices)
    n = len(sorted_prices)
    median_price = sorted_prices[n // 2] if n % 2 == 1 else (sorted_prices[n // 2 - 1] + sorted_prices[n // 2]) / 2
    
    # Calculate Q1 and Q3 for IQR
    q1_index = n // 4
    q3_index = 3 * n // 4
    q1 = sorted_prices[q1_index]
    q3 = sorted_prices[q3_index]
    iqr = q3 - q1
    
    # Define reasonable price range (exclude extreme outliers)
    # Use 1.5 * IQR method (standard outlier detection)
    lower_bound = max(0, q1 - 1.5 * iqr)
    upper_bound = q3 + 1.5 * iqr
    
    # Filter products with relatable prices (within reasonable range)
    relatable_products = [
        p for p in rated_products
        if p.price is not None and p.price > 0 and lower_bound <= p.price <= upper_bound
    ]
    
    if not relatable_products:
        # If filtering removed all products, use all rated products
        logging.getLogger(__name__).info(
            "No products within price range [%.2f, %.2f], using all rated products", 
            lower_bound, upper_bound
        )
        relatable_products = rated_products
    
    # Calculate scores for relatable products
    min_price = min(p.price for p in relatable_products if p.price is not None and p.price > 0)

    for p in relatable_products:
        price_score = (min_price / p.price) if p.price and p.price > 0 else 0
        rating_score = (p.rating / 5.0) if p.rating else 0
        p.final_score = round((price_score * 0.7) + (rating_score * 0.3), 4)
        if p.final_score >= 0.8:
            p.recommendation = "Excellent Deal! Buy Now"
        elif p.final_score >= 0.6:
            p.recommendation = "Good Deal"
        else:
            p.recommendation = "Consider Waiting"

    return sorted(relatable_products, key=lambda x: x.final_score or 0, reverse=True)


async def _scrape_amazon(query: str, crawler: AsyncWebCrawler) -> List[Product]:
    """Scrape only the first page of Amazon search results using LLMExtractionStrategy.

    Returns a list of Product objects extracted from the first search page.
    """
    products: List[Product] = []
    base_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"

    # First try a CSS/JSON extraction strategy (like your working example) which is faster and
    # doesn't require LLM calls. Build a small schema for product title and price.
    css_schema = {
        "name": "Product Block",
        "baseSelector": 'div.s-result-item',
        "fields": [
            {"name": "title", "selector": "h2 a span, span.a-size-medium", "type": "text"},
            {"name": "price", "selector": ".a-price .a-offscreen, .a-price-whole", "type": "text"},
            {"name": "original_price", "selector": "span.a-text-price span.a-offscreen", "type": "text"},
            {"name": "deal_label", "selector": "span.savingsPercentage, span.a-badge-text", "type": "text"},
            {"name": "image", "selector": "img.s-image", "type": "image"},
            {"name": "product_url", "selector": "a.a-link-normal.s-no-outline", "type": "href"},
            {"name": "rating", "selector": "span.a-icon-alt", "type": "text"},
        ],
    }

    strategy = JsonCssExtractionStrategy(css_schema)

    # Prepare pagination and session parameters similar to user's working script
    session_name = f"amazon_{query.replace(' ', '_')}"
    load_nextpage_js = ["const el = document.querySelector('.s-pagination-item.s-pagination-next'); if (el) el.click();"]
    # wait for simple list-item count using a simple selector
    wait_for_code = "() => document.querySelectorAll('div.s-result-item').length > 6"

    items = []
    # Only crawl the first page per user's requirement
    crawler_config = CrawlerRunConfig(
        url=base_url,
        js_only=False,
        extraction_strategy=strategy,
        css_selector='div.s-result-item',
        session_id=session_name,
        cache_mode=CacheMode.BYPASS,
        exclude_external_links=True,
        exclude_social_media_links=True,
    )

    try:
        result = await crawler.arun(url=base_url, config=crawler_config)
    except Exception:
        result = None

    if result and getattr(result, 'success', None) is not False:
        try:
            if getattr(result, 'extracted_content', None):
                batch = json.loads(result.extracted_content)
            else:
                batch = getattr(result, 'extracted_data', None) or getattr(result, 'items', None) or []
        except Exception:
            batch = getattr(result, 'extracted_data', None) or getattr(result, 'items', None) or []

        if batch:
            if isinstance(batch, list):
                items.extend(batch)
            else:
                items.append(batch)
        try:
            logging.getLogger(__name__).debug("_scrape_amazon: extracted items count=%d", len(items))
            if items and isinstance(items[0], dict):
                logging.getLogger(__name__).debug("_scrape_amazon: sample item keys=%s", list(items[0].keys()))
        except Exception:
            pass


    # If Crawl4AI returned items, normalize them deterministically (no LLM required)
    if items:
        try:
            # Try to enrich raw items with local parse to capture URLs/ratings when possible
            try:
                local_parsed = await asyncio.to_thread(_scrape_amazon_local_sync, query)
            except Exception:
                local_parsed = []
            # Combine Crawl4AI items with local parsed dicts so deterministic normalizer can pick up urls/ratings
            combined = list(items)
            if local_parsed:
                combined.extend([p.dict() for p in local_parsed])
            det = deterministic_normalize_items(combined, 'Amazon', query)
            if det:
                logging.getLogger(__name__).info("Deterministic normalize used for Amazon: %d items", len(det))
                return det  # Return all normalized products, not just the most relevant
        except Exception:
            logging.getLogger(__name__).exception("Deterministic normalization failed for Amazon")
            pass

    if not items:
        # Try Playwright-based scraper (headful) for JS-heavy or bot-protected pages
        try:
            pw_items = await _scrape_amazon_playwright(query)
            if pw_items:
                return pw_items
        except Exception:
            pass

        try:
            return await asyncio.to_thread(_scrape_amazon_local_sync, query)
        except Exception:
            return products

    for item in items:
        try:
            if isinstance(item, dict):
                title = item.get('title') or item.get('product_name') or item.get('name')
                price_text = item.get('price') or item.get('price_text') or item.get('amount')
                url = item.get('product_url') or item.get('url')
                img = item.get('image') or item.get('image_url')
                original_price = item.get('original_price')
                deal_label = item.get('deal_label')
                rating_text = item.get('rating')
            else:
                d = item.__dict__
                title = d.get('title') or d.get('product_name') or d.get('name')
                price_text = d.get('price') or d.get('price_text') or d.get('amount')
                url = d.get('product_url') or d.get('url')
                img = d.get('image') or d.get('image_url')
                original_price = d.get('original_price')
                deal_label = d.get('deal_label')
                rating_text = d.get('rating')

            if not title and url:
                title = url.split('/')[-1].replace('-', ' ').replace('.html', '')

            price_val = 0.0
            if price_text:
                try:
                    price_val = float(re.sub(r"[^0-9.]", "", str(price_text)))
                except Exception:
                    price_val = 0.0

            # Compose discount info
            discount_parts = []
            if original_price:
                discount_parts.append(f"Original: {original_price}")
            if deal_label:
                discount_parts.append(str(deal_label))
            # Calculate discount percentage if possible
            discount_percent = None
            if original_price and price_val:
                try:
                    orig_val = float(re.sub(r"[^0-9.]", "", str(original_price)))
                    if orig_val > price_val:
                        percent = int(round((orig_val - price_val) / orig_val * 100))
                        discount_percent = f"{percent}% off"
                        discount_parts.append(discount_percent)
                except Exception:
                    pass
            discount = " | ".join(discount_parts) if discount_parts else None

            rating_val = None
            if rating_text:
                try:
                    rating_val = float(re.sub(r"[^0-9.]", "", str(rating_text)))
                except Exception:
                    rating_val = None

            if title:
                products.append(Product(product_name=title, price=price_val or 0.0, rating=rating_val, product_url=url, image_url=img, retailer='Amazon', discount=discount))
        except Exception:
            continue

    return products


async def _llm_extract_products(raw_items: List[dict], source: str, query: str) -> List[Product]:
    """Normalize a list of raw item dicts into Product models using an LLM.

    This uses a different model than the relevance LLM to separate concerns.
    Returns list[Product] or empty list on failure.
    """
    if not raw_items:
        return []

    # Build a compact prompt that supplies the list of raw items and asks the LLM to
    # return a JSON array of objects matching the Product model fields.
    numbered = []
    for i, it in enumerate(raw_items[:20]):
        # Keep prompt size reasonable
        try:
            title = it.get('title') or it.get('product_name') or it.get('name') or ''
            price = it.get('price') or it.get('price_text') or it.get('amount') or ''
            url = it.get('product_url') or it.get('url') or ''
            numbered.append(f"{i+1}. title: {title} | price: {price} | url: {url}")
        except Exception:
            continue

    prompt = (
        f"You are given a user search '{query}'.\n"
        f"Normalize the following raw product lines into a JSON array of objects with keys: product_name (string), price (number, INR), rating (number 0-5 or null), product_url (string or null), image_url (string or null), retailer (string).\n"
        f"Items:\n" + "\n".join(numbered) + "\n\nReturn only the JSON array."
    )

    # Dev stub mode: return a deterministic mapping without calling external LLMs.
    if DEV_LLM_STUB:
        out: List[Product] = []
        for i, it in enumerate(raw_items[:8]):
            try:
                title = (it.get('title') or it.get('product_name') or it.get('name') or f"item_{i}")
                price_text = it.get('price') or it.get('price_text') or it.get('amount') or '0'
                try:
                    price_val = float(re.sub(r"[^0-9.]", "", str(price_text))) if price_text else 0.0
                except Exception:
                    price_val = 0.0
                out.append(Product(product_name=title, price=price_val or 0.0, rating=None, product_url=it.get('product_url') or it.get('url'), image_url=it.get('image') or it.get('image_url'), retailer=source))
            except Exception:
                continue
        return out

    # Try primary then fallback OpenAI keys with exponential backoff and jitter
    async def call_openai_with_key_backoff(api_key: str, max_attempts: int = 4) -> Optional[str]:
        client = AsyncOpenAI(api_key=api_key)
        attempt = 0
        try:
            while attempt < max_attempts:
                attempt += 1
                try:
                    resp = await client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.0,
                        max_tokens=512,
                    )
                    if resp and getattr(resp, 'choices', None):
                        choice = resp.choices[0]
                        if hasattr(choice, 'message') and getattr(choice.message, 'content', None):
                            return choice.message.content
                        if getattr(choice, 'text', None):
                            return choice.text
                    return None
                except Exception as e:
                    # If rate-limited or transient, backoff and retry; otherwise re-raise after attempts
                    wait = (1.5 ** attempt) + random.uniform(0, 0.6)
                    await asyncio.sleep(wait)
                    continue
            return None
        finally:
            if hasattr(client, 'aclose'):
                try:
                    await client.aclose()
                except Exception:
                    pass

    # Check cache first
    cached = _llm_cache_get(prompt)
    if cached:
        text = cached
    else:
        text = None
        for key in [OPENAI_API_KEY] + ([OPENAI_API_KEY_FALLBACK] if OPENAI_API_KEY_FALLBACK else []):
            try:
                text = await call_openai_with_key_backoff(key)
            except Exception:
                text = None
            if text:
                break
        if text:
            try:
                _llm_cache_set(prompt, text)
            except Exception:
                pass

    # If still no text and Gemini is available, call Gemini
    if not text and GEMINI_API_KEY:
        # check cache for gemini too
        cached_g = _llm_cache_get(prompt + "|gemini")
        if cached_g:
            text = cached_g
        else:
            try:
                # gem = await _call_gemini(GEMINI_API_KEY, prompt)  # Disabled: function not defined
                # text = gem  # Disabled: 'gem' is not defined
                if text:
                    _llm_cache_set(prompt + "|gemini", text)
            except Exception:
                text = None

    if not text:
        return []

    # Attempt to parse JSON from the LLM response
    try:
        # LLMs sometimes wrap JSON in code fences; strip them
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip())
        data = json.loads(cleaned)
        out: List[Product] = []
        if isinstance(data, list):
            for it in data:
                try:
                    name = it.get('product_name') or it.get('title') or it.get('name')
                    price = it.get('price')
                    try:
                        price_val = float(re.sub(r"[^0-9.]", "", str(price))) if price is not None and str(price).strip() != '' else 0.0
                    except Exception:
                        price_val = 0.0
                    rating = it.get('rating')
                    try:
                        rating_val = float(rating) if rating is not None else None
                    except Exception:
                        rating_val = None
                    url = it.get('product_url') or it.get('url')
                    img = it.get('image_url') or it.get('image')
                    retailer = it.get('retailer') or source
                    if name:
                        out.append(Product(product_name=name, price=price_val or 0.0, rating=rating_val, product_url=url, image_url=img, retailer=retailer))
                except Exception:
                    continue
        return out
    except Exception:
        return []


def _scrape_amazon_local_sync(query: str) -> List[Product]:
    """Local synchronous Amazon scraper using requests + BeautifulSoup for first page only."""
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    session = requests.Session()
    session.headers.update(_build_headers())
    resp = _requests_with_retries(url, headers=session.headers, timeout=15, session=session)
    if resp is None:
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Main product containers: robust multi-selector for Amazon search results
    containers = soup.select('div.s-main-slot > div[data-asin][data-component-type="s-search-result"]')
    # Fallbacks for alternate layouts
    if not containers:
        containers = soup.select('div.s-result-item[data-asin]')
    if not containers:
        containers = soup.select('div.s-main-slot div[data-asin]')
    # If still empty, try JSON-LD parsing
    if not containers:
        jl = _parse_jsonld_products(resp.text)
        if jl:
            return jl

    products: List[Product] = []
    import logging
    for c in containers[:16]:
        try:
            # Title: robust multi-selector
            title_tag = (
                c.select_one('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 > a > span') or
                c.select_one('h2 > a > span') or
                c.select_one('span.a-size-medium') or
                c.select_one('h2 > span')
            )
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            # Price: robust multi-selector
            price_tag = (
                c.select_one('span.a-price > span.a-offscreen') or
                c.select_one('span.a-price-whole') or
                c.select_one('span.a-price-fraction')
            )
            price = None
            if price_tag:
                price_text = price_tag.get_text(strip=True)
                try:
                    price = float(re.sub(r"[^0-9.]", "", price_text))
                except Exception:
                    price = None

            # Rating: robust multi-selector
            rating = None
            rating_tag = (
                c.select_one('span.a-icon-alt') or
                c.select_one('span.a-size-base.a-color-base') or
                c.select_one('span.a-size-small.a-color-base')
            )
            if rating_tag:
                rating_text = rating_tag.get_text(strip=True)
                m = re.search(r"([0-9.]+)", rating_text)
                if m:
                    try:
                        rating = float(m.group(1))
                    except Exception:
                        rating = None

            # Product URL: prefer h2 > a, then any product link
            link_tag = (
                c.select_one('h2 > a') or
                c.select_one('a.a-link-normal.s-no-outline') or
                c.select_one('a.a-link-normal')
            )
            product_url = urljoin('https://www.amazon.in', link_tag['href']) if link_tag and link_tag.get('href') else None

            # Image URL: robust multi-selector
            img_tag = (
                c.select_one('img.s-image') or
                c.select_one('img[data-image-latency]') or
                c.select_one('img')
            )
            image_url = img_tag.get('src') if img_tag and img_tag.get('src') else None

            logging.getLogger(__name__).debug(f"Amazon local: title={title!r}, product_url={product_url!r}, image_url={image_url!r}, rating={rating!r}")

            if title:
                products.append(Product(product_name=title, price=price or 0.0, rating=rating, product_url=product_url, image_url=image_url, retailer='Amazon'))
        except Exception as e:
            logging.getLogger(__name__).exception(f"Amazon local: Exception parsing product card: {e}")
    return products


async def _scrape_amazon_playwright(query: str) -> List[Product]:
    """Use Playwright to load the Amazon search page (headful) and return parsed Product list."""
    # Import lazily to avoid requiring Playwright during import time
    try:
        from playwright.async_api import async_playwright
    except Exception:
        return []

    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    products: List[Product] = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=_build_headers().get('User-Agent'))
            page = await context.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=20000)
            # Small wait for lazy content
            await page.wait_for_timeout(800)
            html = await page.content()
            # Parse HTML with the same local parser
            products = await asyncio.to_thread(lambda: _parse_html_products(html, 'amazon'))
            await context.close()
            await browser.close()
    except Exception:
        return []
    return products


async def _scrape_flipkart(query: str, crawler: AsyncWebCrawler) -> List[Product]:
    """Scrape only the first page of Flipkart search results using LLMExtractionStrategy.

    Returns a list of Product objects extracted from the first search page.
    """
    products: List[Product] = []
    base_url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"

    # First try a CSS/JSON extraction strategy for Flipkart
    css_schema = {
        "name": "Product Block",
        # broaden base selector to match multiple Flipkart search layouts
        "baseSelector": 'div._1AtVbE div._2kHMtA, div._13oc-S, div._1AtVbE ._4ddWXP',
        "fields": [
            {"name": "title", "selector": "div._4rR01T, a.s1Q9rs, a.IRpwTa, div._2B099V", "type": "text"},
            {"name": "price", "selector": "div._30jeq3, div._25b18c, div._1vC4OE, span._2b3S0g", "type": "text"},
        ],
    }

    strategy = JsonCssExtractionStrategy(css_schema)

    session_name = f"flipkart_{query.replace(' ', '_')}"
    # Flipkart next page button class can be '_1LKTO3' or '._1LKTO3'. Use querySelector in JS
    # more robust next-page JS: scroll, then find an anchor/button with 'next' text or aria-label and click it
    load_nextpage_js = [
        "(function(){ window.scrollTo({top: document.body.scrollHeight});\nconst next = Array.from(document.querySelectorAll('a')).find(a=>/\\bnext\\b/i.test(a.textContent) || (a.getAttribute && /next/i.test(a.getAttribute('aria-label'))));\nif(next){ next.click(); return true;}\nconst btn = document.querySelector('button._2KpZ6l._2U9uOA._3v1-ww'); if(btn){ btn.click(); return true;}\nreturn false; })()"
    ]
    # Wait until the page loads and at least one product container exists
    wait_for_code = "() => document.readyState === 'complete' && document.querySelectorAll('div._13oc-S').length > 0"

    # Only fetch the first results page for Flipkart (no pagination)
    items: List[dict] = []
    crawler_config = CrawlerRunConfig(
        url=base_url,
        js_only=False,
        extraction_strategy=strategy,
        css_selector='div._13oc-S',
        session_id=session_name,
        cache_mode=CacheMode.BYPASS,
        exclude_external_links=True,
        exclude_social_media_links=True,
    )
    try:
        result = await crawler.arun(url=base_url, config=crawler_config)
    except Exception:
        result = None

    if result and getattr(result, 'success', None) is not False:
        try:
            if getattr(result, 'extracted_content', None):
                batch = json.loads(result.extracted_content)
            else:
                batch = getattr(result, 'extracted_data', None) or getattr(result, 'items', None) or []
        except Exception:
            batch = getattr(result, 'extracted_data', None) or getattr(result, 'items', None) or []

        if batch:
            if isinstance(batch, list):
                items.extend(batch)
            else:
                items.append(batch)
        try:
            logging.getLogger(__name__).debug("_scrape_flipkart: extracted items count=%d", len(items))
            if items and isinstance(items[0], dict):
                logging.getLogger(__name__).debug("_scrape_flipkart: sample item keys=%s", list(items[0].keys()))
        except Exception:
            pass

    # If Crawl4AI found nothing, try a local sync parser early (this helps when the page renders JSON-LD or
    # different layouts that the JsonCss strategy missed). This avoids waiting for Playwright and increases
    # chances of capturing product_url from structured data.
    if not items:
        try:
            local_parsed = await asyncio.to_thread(_scrape_flipkart_local_sync, query)
            if local_parsed:
                logging.getLogger(__name__).info("_scrape_flipkart: local sync parsed %d items as fallback", len(local_parsed))
                # Return local_parsed directly (they are Product objects)
                return local_parsed
        except Exception:
            logging.getLogger(__name__).exception("_scrape_flipkart: local sync fallback failed")

    # If no items found via JsonCss, try LLM strategy then Playwright then local sync
    if not items:
        # LLM extraction via Crawl4AI as fallback
        instruction = (
            "From the HTML content of a single product container, extract the following fields:"
            " product_name (string), price (numeric INR), rating (numeric out of 5),"
            " product_url (string), image_url (string). Return a JSON object matching the Product model."
        )

        llm_strategy = LLMExtractionStrategy(
            model=Product,
            instruction=instruction,
            model_kwargs={"openai_api_key": OPENAI_API_KEY}
        )

        config = CrawlerRunConfig(
            url=base_url,
            css_selector='div._13oc-S',
            extraction_strategy=llm_strategy,
            cache_mode=CacheMode.BYPASS,
            exclude_external_links=True,
            exclude_social_media_links=True,
        )

        try:
            result = await crawler.arun(url=base_url, config=config)
        except Exception:
            result = None

        if result:
            items = getattr(result, 'extracted_data', None) or getattr(result, 'items', None) or []


    # If Crawl4AI returned items, normalize them deterministically (no LLM required)
    if items:
        try:
            try:
                local_parsed = await asyncio.to_thread(_scrape_flipkart_local_sync, query)
            except Exception:
                local_parsed = []
            combined = list(items)
            if local_parsed:
                combined.extend([p.dict() for p in local_parsed])
            det = deterministic_normalize_items(combined, 'Flipkart', query)
            if det:
                logging.getLogger(__name__).info("Deterministic normalize used for Flipkart: %d items", len(det))
                return det  # Return all normalized Flipkart products
        except Exception:
            logging.getLogger(__name__).exception("Deterministic normalization failed for Flipkart")
            pass

    if not items:
        try:
            pw_items = await _scrape_flipkart_playwright(query)
            if pw_items:
                return pw_items
        except Exception:
            pass

        try:
            return await asyncio.to_thread(_scrape_flipkart_local_sync, query)
        except Exception:
            return products
            # If no HTML containers found, try JSON-LD parsing for Flipkart pages
            if not containers:
                jl = _parse_jsonld_products(html)
                if jl:
                    return jl

    # Map items (dicts) to Product model
    for item in items:
        try:
            if isinstance(item, dict):
                title = item.get('title') or item.get('product_name') or item.get('name')
                price_text = item.get('price') or item.get('price_text') or item.get('amount')
                url = item.get('product_url') or item.get('url')
                img = item.get('image') or item.get('image_url')
            else:
                d = item.__dict__
                title = d.get('title') or d.get('product_name') or d.get('name')
                price_text = d.get('price') or d.get('price_text') or d.get('amount')
                url = d.get('product_url') or d.get('url')
                img = d.get('image') or d.get('image_url')

            price_val = 0.0
            if price_text:
                try:
                    price_val = float(re.sub(r"[^0-9.]", "", str(price_text)))
                except Exception:
                    {"name": "original_price", "selector": ".yRaY8j.ZYYwLA", "type": "text"},
                    {"name": "discount_percent", "selector": ".UkUFwK span", "type": "text"},
                    {"name": "discount_label", "selector": ".yiggsN.O5Fpg8", "type": "text"},

            # Filter out common non-title captures (discount badges, placeholders)
            if not title:
                continue
            title_clean = title.strip()
            # skip titles that look like a percentage or only numbers/symbols
            if re.match(r'^[\d\-\%\s,]+$', title_clean):
                continue
            # skip extremely short or non-alpha titles
            if len(title_clean) < 6 or not re.search(r'[A-Za-z]', title_clean):
                continue

            products.append(Product(product_name=title_clean, price=price_val or 0.0, rating=None, product_url=url, image_url=img, retailer='Flipkart'))
        except Exception:
            continue

    return products


async def _scrape_flipkart_playwright(query: str) -> List[Product]:
    """Use Playwright to load the Flipkart search page (headful) and return parsed Product list."""
    try:
        from playwright.async_api import async_playwright
    except Exception:
        return []

    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    products: List[Product] = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=_build_headers().get('User-Agent'))
            page = await context.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=20000)
            await page.wait_for_timeout(800)
            html = await page.content()
            products = await asyncio.to_thread(lambda: _parse_html_products(html, 'flipkart'))
            await context.close()
            await browser.close()
    except Exception:
        return []
    return products


def _parse_html_products(html: str, source: str) -> List[Product]:
    """Shared HTML parsing entrypoint used by Playwright fetches. source: 'amazon' or 'flipkart' or 'json-ld'"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        if source == 'amazon':
            # broaden possible container selectors to catch different Amazon layouts
            selectors = [
                'div[data-component-type="s-search-result"]',
                'div.s-result-item',
                'div.s-main-slot div[data-asin]',
                'div.sg-row div.s-result-item',
                'div[data-asin]'
            ]
            containers = []
            for sel in selectors:
                found = soup.select(sel)
                if found:
                    containers = found
                    break
            if not containers:
                return _parse_jsonld_products(html)
            products: List[Product] = []
            for c in containers[:12]:
                try:
                    title_tag = c.select_one('h2 a span') or c.select_one('span.a-size-medium')
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)
                    price_tag = c.select_one('.a-price .a-offscreen') or c.select_one('.a-price-whole')
                    price = None
                    if price_tag:
                        price_text = price_tag.get_text(strip=True)
                        try:
                            price = float(re.sub(r"[^0-9.]", "", price_text))
                        except Exception:
                            price = None
                    rating_tag = c.select_one('.a-icon-alt') or c.select_one('.a-icon-star .a-icon-alt')
                    rating = None
                    if rating_tag:
                        m = re.search(r"([0-9.]+)", rating_tag.get_text())
                        if m:
                            try:
                                rating = float(m.group(1))
                            except Exception:
                                rating = None
                    link_tag = c.select_one('h2 a')
                    product_url = urljoin('https://www.amazon.in', link_tag['href']) if link_tag and link_tag.get('href') else None
                    img_tag = c.select_one('img.s-image')
                    image_url = img_tag.get('src') if img_tag and img_tag.get('src') else None
                    if title:
                        products.append(Product(product_name=title, price=price or 0.0, rating=rating, product_url=product_url, image_url=image_url, retailer='Amazon'))
                except Exception:
                    continue
            return products

        if source == 'flipkart':
            selectors = [
                'div._1AtVbE div._13oc-S',
                'div._1AtVbE ._4ddWXP',
                'div._1AtVbE div._2kHMtA',
                'div._13oc-S',
                'div._1AtVbE',
                # other common Flipkart containers
                'div._2kHMtA',
                'div._3O0U0u'
            ]
            containers = []
            for sel in selectors:
                found = soup.select(sel)
                if found:
                    containers = found
                    break
            if not containers:
                return _parse_jsonld_products(html)
            products: List[Product] = []
            for c in containers[:12]:
                try:
                    title_tag = c.select_one('div._4rR01T') or c.select_one('a.s1Q9rs') or c.select_one('a.IRpwTa') or c.select_one('a')
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)
                    price_tag = c.select_one('div._30jeq3') or c.select_one('div._25b18c')
                    price = None
                    if price_tag:
                        price_text = price_tag.get_text(strip=True)
                        try:
                            price = float(re.sub(r"[^0-9.]", "", price_text))
                        except Exception:
                            price = None
                    # rating may appear as '4.3' or as text; parse robustly
                    rating_tag = c.select_one('div._3LWZlK') or c.select_one('div._2b4-LK') or c.select_one('span._1lRcqv')
                    rating = None
                    if rating_tag and rating_tag.get_text(strip=True):
                        rt = rating_tag.get_text(strip=True)
                        m = re.search(r"([0-9]+\.?[0-9]*)", rt)
                        if m:
                            try:
                                rating = float(m.group(1))
                            except Exception:
                                rating = None
                    link_tag = c.select_one('a._1fQZEK') or c.select_one('a.s1Q9rs') or c.select_one('a')
                    product_url = None
                    if link_tag and link_tag.get('href'):
                        product_url = urljoin('https://www.flipkart.com', link_tag['href'])
                    img_tag = c.select_one('img._396cs4') or c.select_one('img')
                    image_url = img_tag.get('src') if img_tag and img_tag.get('src') else None
                    title_clean = title.strip()
                    if re.match(r'^[\d\-\%\s,]+$', title_clean):
                        continue
                    if len(title_clean) < 6 or not re.search(r'[A-Za-z]', title_clean):
                        continue
                    products.append(Product(product_name=title_clean, price=price or 0.0, rating=rating, product_url=product_url, image_url=image_url, retailer='Flipkart'))
                except Exception:
                    continue
            return products
    except Exception:
        return []
    return []


def _scrape_flipkart_local_sync(query: str) -> List[Product]:
    """Local synchronous Flipkart scraper using requests + BeautifulSoup for first page only."""
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    session = requests.Session()
    session.headers.update(_build_headers())
    resp = _requests_with_retries(url, headers=session.headers, timeout=15, session=session)
    if resp is None:
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Try multiple container selectors to catch different Flipkart layouts
    selectors = [
        'div._1AtVbE div._13oc-S',
        'div._1AtVbE ._4ddWXP',
        'div._1AtVbE div._2kHMtA',
        'div._13oc-S',
        'div._1AtVbE',
        'div.tUxRFH',
        'div.tUxRFH[data-tkid]',
    ]
    containers = []
    used_sel = None
    for sel in selectors:
        found = soup.select(sel)
        if found:
            containers = found
            used_sel = sel
            break

    try:
        import logging
        logging.getLogger(__name__).debug(f"Flipkart local: using selector '{used_sel}' found {len(containers)} containers")
    except Exception:
        pass

    products: List[Product] = []
    # If no containers found via selectors, try JSON-LD structured data as a fallback
    if not containers:
        try:
            jl = _parse_jsonld_products(resp.text)
            if jl:
                logging.getLogger(__name__).debug("Flipkart local: parsed %d products from JSON-LD fallback", len(jl))
                return jl
        except Exception:
            pass

    import logging
    for c in containers[:12]:
        try:
            # Title
            title_tag = (
                c.select_one('div._4rR01T') or
                c.select_one('a.s1Q9rs') or
                c.select_one('a.IRpwTa') or
                c.select_one('div.KzDlHZ') or
                c.select_one('div.KzDlHZ') or
                c.select_one('div._2B099V')
            )
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            # Price
            price_tag = (
                c.select_one('div._30jeq3') or
                c.select_one('div._25b18c') or
                c.select_one('div.Nx9bqj._4b5DiR') or
                c.select_one('div.yRaY8j.ZYYwLA') or
                c.select_one('div._1vC4OE') or
                c.select_one('span._2b3S0g')
            )
            price = None
            if price_tag:
                price_text = price_tag.get_text(strip=True)
                try:
                    price = float(re.sub(r"[^0-9.]", "", price_text))
                except Exception:
                    price = None

            # Rating
            rating_tag = (
                c.select_one('div._3LWZlK') or
                c.select_one('div._2b4-LK') or
                c.select_one('div.XQDdHH')
            )
            rating = None
            if rating_tag:
                try:
                    rating_text = rating_tag.get_text(strip=True)
                    m = re.match(r"([0-9]+\.?[0-9]*)", rating_text)
                    if m:
                        rating = float(m.group(1))
                except Exception:
                    rating = None

            # Product URL
            link_tag = (
                c.select_one('a.CGtC98') or
                c.select_one('a._1fQZEK') or
                c.select_one('a.s1Q9rs') or
                c.select_one('a.IRpwTa') or
                c.select_one('a')
            )
            product_url = urljoin('https://www.flipkart.com', link_tag['href']) if link_tag and link_tag.get('href') else None

            # Image URL
            img_tag = (
                c.select_one('img.DByuf4') or
                c.select_one('img._396cs4') or
                c.select_one('img')
            )
            image_url = img_tag.get('src') if img_tag and img_tag.get('src') else None

            logging.getLogger(__name__).debug(f"Flipkart local: title={title!r}, product_url={product_url!r}, image_url={image_url!r}, rating={rating!r}, price={price!r}")

            products.append(Product(product_name=title, price=price or 0.0, rating=rating, product_url=product_url, image_url=image_url, retailer='Flipkart'))
        except Exception:
            continue
    return products


def _parse_jsonld_products(html: str) -> List[Product]:
    """Parse application/ld+json blocks for Product entries and return Product list."""
    out: List[Product] = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # Find script tags that explicitly declare JSON-LD or appear to contain JSON-LD payloads
        scripts = []
        for s in soup.find_all('script'):
            t = (s.get('type') or '').lower()
            txt = (s.string or s.text or '').strip()
            if 'application/ld+json' in t:
                scripts.append(s)
                continue
            # Heuristic: script contains JSON-LD if it includes common JSON-LD markers
            if txt.startswith('{') or txt.startswith('['):
                if '@context' in txt or '"@type"' in txt or 'ItemList' in txt or 'Product' in txt:
                    scripts.append(s)
                    continue
        for s in scripts:
            try:
                txt = s.string or s.text or ''
                # Try direct load first
                try:
                    data = json.loads(txt)
                except Exception:
                    # Remove C-style comments and try again
                    cleaned = re.sub(r'/\*.*?\*/', '', txt, flags=re.S)
                    # Remove trailing commas in objects/arrays (simple heuristic)
                    cleaned = re.sub(r',\s*([}\]])', r"\1", cleaned)
                    try:
                        data = json.loads(cleaned)
                    except Exception:
                        # As a last resort, extract the first {...} block
                        m = re.search(r'\{.*\}', cleaned, flags=re.S)
                        if m:
                            try:
                                data = json.loads(m.group(0))
                            except Exception:
                                continue
                        else:
                            continue
            except Exception:
                continue
            # If the top-level is an ItemList, extract its itemListElement entries
            if isinstance(data, dict) and (str(data.get('@type') or '').lower().find('itemlist') != -1) and data.get('itemListElement'):
                entries = data.get('itemListElement') or []
            else:
                entries = data if isinstance(data, list) else [data]

            for it in entries:
                try:
                    # Some ItemList entries are ListItem wrappers with a nested item or name/url fields
                    if not isinstance(it, dict):
                        continue
                    # If it's a ListItem wrapper, try to unwrap
                    if it.get('@type') and 'listitem' in str(it.get('@type')).lower():
                        # common shapes: {'@type':'ListItem','position':1,'url':'...','name':'...'}
                        name = it.get('name') or (it.get('item') or {}).get('name')
                        url = it.get('url') or (it.get('item') or {}).get('url')
                        image = (it.get('item') or {}).get('image')
                        price = None
                        rating = None
                        if name:
                            out.append(Product(product_name=name, price=price or 0.0, rating=rating, product_url=url, image_url=image, retailer='json-ld'))
                        continue

                    typ = it.get('@type') or it.get('type')
                    # If it's a product-like dict, proceed
                    name = it.get('name')
                    image = it.get('image')
                    url = it.get('url')
                    price = None
                    if it.get('offers'):
                        offers = it.get('offers')
                        if isinstance(offers, list):
                            offers = offers[0]
                        price_val = offers.get('price') if isinstance(offers, dict) else None
                        if price_val:
                            try:
                                price = float(re.sub(r"[^0-9.]", "", str(price_val)))
                            except Exception:
                                price = None
                    rating = None
                    if it.get('aggregateRating') and isinstance(it.get('aggregateRating'), dict):
                        try:
                            rating = float(it['aggregateRating'].get('ratingValue'))
                        except Exception:
                            rating = None
                    if name:
                        out.append(Product(product_name=name, price=price or 0.0, rating=rating, product_url=url, image_url=image, retailer='json-ld'))
                except Exception:
                    continue
    except Exception:
        return []
    return out


def deterministic_normalize_items(raw_items: List[dict], source: str, query: str) -> List[Product]:
    """Deterministically normalize raw items (from Crawl4AI JsonCss or LLMExtractionStrategy output)
    without calling external LLMs. This uses best-effort field extraction and fallbacks.
    """
    out: List[Product] = []
    for it in raw_items[:24]:
        try:
            if isinstance(it, dict):
                title = (it.get('title') or it.get('product_name') or it.get('name') or '').strip()
                price_text = it.get('price') or it.get('price_text') or it.get('amount') or ''
                url = it.get('product_url') or it.get('url') or it.get('link') or None
                img = it.get('image') or it.get('image_url') or it.get('thumbnail') or None
                rating = it.get('rating') or it.get('rating_value') or None
            else:
                d = getattr(it, '__dict__', {})
                title = (d.get('title') or d.get('product_name') or d.get('name') or '').strip()
                price_text = d.get('price') or d.get('price_text') or d.get('amount') or ''
                url = d.get('product_url') or d.get('url') or d.get('link') or None
                img = d.get('image') or d.get('image_url') or d.get('thumbnail') or None
                rating = d.get('rating') or d.get('rating_value') or None

            if not title:
                # skip placeholder or bad captures
                continue

            # normalize price
            price = normalize_price_text(price_text)

            # normalize rating
            rating_val = None
            if rating is not None:
                try:
                    rating_val = float(re.sub(r"[^0-9.]+", "", str(rating)))
                except Exception:
                    rating_val = None

            # keep only reasonable titles
            title_clean = re.sub(r"\s+", " ", title)
            if len(title_clean) < 4 or not re.search(r'[A-Za-z]', title_clean):
                continue

            # Normalize relative URLs to absolute using retailer base
            try:
                if url and url.startswith('/'):
                    base = 'https://www.flipkart.com' if 'flipkart' in (source or '').lower() else 'https://www.amazon.in'
                    url = urljoin(base, url)
                if img and img.startswith('/'):
                    base = 'https://www.flipkart.com' if 'flipkart' in (source or '').lower() else 'https://www.amazon.in'
                    img = urljoin(base, img)
            except Exception:
                pass

            out.append(Product(product_name=title_clean, price=price or 0.0, rating=rating_val, product_url=url, image_url=img, retailer=source))
        except Exception:
            continue

    return out


def enrich_raw_with_parsed(raw_items: List[dict], parsed_products: List[Product]) -> List[dict]:
    """Return a new list of raw_items where we try to enrich missing url/rating/image by fuzzy-matching
    against parsed_products (from local BS4 parser)."""
    enriched = []
    parsed_titles = [(p.product_name or '').lower() for p in parsed_products]
    for it in raw_items:
        try:
            if isinstance(it, dict):
                title = (it.get('title') or it.get('product_name') or it.get('name') or '').strip()
            else:
                title = getattr(it, 'title', '') or getattr(it, 'product_name', '') or getattr(it, 'name', '')
            t = (title or '').lower()
            best_idx = None
            best_ratio = 0.0
            for i, pt in enumerate(parsed_titles):
                if not t or not pt:
                    continue
                r = difflib.SequenceMatcher(a=t, b=pt).ratio()
                if r > best_ratio:
                    best_ratio = r
                    best_idx = i

            out = dict(it) if isinstance(it, dict) else dict(getattr(it, '__dict__', {}))
            if best_idx is not None and best_ratio >= 0.45:
                p = parsed_products[best_idx]
                try:
                    logging.getLogger(__name__).debug("enrich_raw_with_parsed: matched raw=' %s ' -> parsed='%s' ratio=%.3f", title, p.product_name, best_ratio)
                except Exception:
                    pass
                # only add fields if missing
                if not out.get('product_url') and p.product_url:
                    out['product_url'] = p.product_url
                if not out.get('image') and p.image_url:
                    out['image'] = p.image_url
                if not out.get('rating') and p.rating is not None:
                    out['rating'] = p.rating
            enriched.append(out)
        except Exception:
            enriched.append(it)
    return enriched


def enrich_products_with_local(products: List[Product], local_parsed: List[Product]) -> List[Product]:
    """Fuzzy-match Product entries to local parsed products and copy product_url, image_url, rating when missing."""
    if not products or not local_parsed:
        return products
    local_titles = [(p.product_name or '').lower() for p in local_parsed]
    out = []
    for p in products:
        try:
            name = (p.product_name or '').lower()
            best_idx = None
            best_ratio = 0.0
            for i, lt in enumerate(local_titles):
                if not name or not lt:
                    continue
                r = difflib.SequenceMatcher(a=name, b=lt).ratio()
                if r > best_ratio:
                    best_ratio = r
                    best_idx = i
            if best_idx is not None and best_ratio >= 0.45:
                lp = local_parsed[best_idx]
                try:
                    logging.getLogger(__name__).debug("enrich_products_with_local: matched '%s' -> '%s' ratio=%.3f", p.product_name, lp.product_name, best_ratio)
                except Exception:
                    pass
                if not p.product_url and lp.product_url:
                    logging.getLogger(__name__).debug("enrich_products_with_local: copying product_url for '%s' -> %s", p.product_name, lp.product_url)
                    p.product_url = lp.product_url
                if not p.image_url and lp.image_url:
                    p.image_url = lp.image_url
                if (p.rating is None or p.rating == 0) and lp.rating is not None:
                    logging.getLogger(__name__).debug("enrich_products_with_local: copying rating for '%s' -> %.2f", p.product_name, lp.rating)
                    p.rating = lp.rating
        except Exception:
            pass
        out.append(p)
    return out


def deterministic_select_most_relevant(query: str, products: List[Product]) -> Optional[Product]:
    """Pick the most relevant product deterministically using token overlap and fuzzy title matching.

    Scoring components:
    - Title similarity via SequenceMatcher (0-1)
    - Token overlap ratio between query tokens and title tokens
    - Prefer lower price when similarity ties
    Returns the single chosen Product.
    """
    if not products:
        return None

    q = query.lower().strip()
    q_tokens = [t for t in re.split(r"\W+", q) if t]
    best = None
    best_score = -1.0

    for p in products:
        name = (p.product_name or '').lower()
        name_tokens = [t for t in re.split(r"\W+", name) if t]

        # fuzzy title similarity
        seq = difflib.SequenceMatcher(a=q, b=name)
        sim = seq.ratio()

        # token overlap (fraction of query tokens in name)
        if q_tokens:
            overlap = sum(1 for t in q_tokens if t in name_tokens) / len(q_tokens)
        else:
            overlap = 0.0

        # combined score: heavier weight to similarity and token overlap
        score = (0.6 * sim) + (0.3 * overlap)

        # small bonuses for having a product URL and rating (prefer complete results)
        if p.product_url:
            score += 0.05
        if p.rating:
            score += 0.05

        # small price bonus: cheaper products get a tiny boost (normalize within found set)
        # we apply price bonus later after collecting min price
        if best is None or score > best_score:
            best = p
            best_score = score

    # tie-breaker using price: if multiple products have near-equal score, pick the cheaper
    close = [p for p in products if abs(((0.6 * difflib.SequenceMatcher(a=q, b=(p.product_name or '').lower()).ratio()) + 0.3 * (sum(1 for t in q_tokens if t in [x for x in re.split(r'\W+', (p.product_name or '').lower()) if x])/len(q_tokens) if q_tokens else 0.0)) - best_score) < 0.02]
    if len(close) > 1:
        # choose minimum price among close matches
        priced = [p for p in close if p.price and p.price > 0]
        if priced:
            return min(priced, key=lambda x: x.price)
        return close[0]

    return best


def deterministic_select_top_k(query: str, products: List[Product], k: int = 3) -> List[Product]:
    """Score all products using the same heuristics as deterministic_select_most_relevant
    and return the top-k products. Preference is given to products that have the
    required fields (product_url, image_url, price, rating)."""
    if not products:
        return []

    q = query.lower().strip()
    q_tokens = [t for t in re.split(r"\W+", q) if t]
    scored = []

    # compute base scores
    for p in products:
        try:
            name = (p.product_name or '').lower()
            name_tokens = [t for t in re.split(r"\W+", name) if t]

            seq = difflib.SequenceMatcher(a=q, b=name).ratio()
            overlap = (sum(1 for t in q_tokens if t in name_tokens) / len(q_tokens)) if q_tokens else 0.0
            score = (0.6 * seq) + (0.3 * overlap)
            if p.product_url:
                score += 0.03
            if p.image_url:
                score += 0.02
            if p.rating:
                score += 0.03
            # small normalization for price presence
            if p.price and p.price > 0:
                score += 0.01
            scored.append((score, p))
        except Exception:
            scored.append((0.0, p))

    # sort descending by score
    scored.sort(key=lambda x: x[0], reverse=True)

    # Prefer products that have all required fields. Build two lists: complete and partial.
    complete = [p for s, p in scored if p.product_url and p.image_url and p.price and (p.rating is not None)]
    partial = [p for s, p in scored if p not in complete]

    result: List[Product] = []
    for p in complete:
        if len(result) >= k:
            break
        result.append(p)

    if len(result) < k:
        for p in partial:
            if len(result) >= k:
                break
            result.append(p)

    return result


def normalize_price_text(price_text: str) -> float:
    """Robustly convert a price-like string into a float (INR assumed).

    Handles common separators, unicode digits, and ranges like '₹12,999 - ₹15,999'.
    Returns 0.0 on failure.
    """
    if not price_text:
        return 0.0
    try:
        s = str(price_text).strip()
        # replace non-breaking spaces and common unicode currency markers
        s = s.replace('\u00a0', ' ')
        # replace common unicode digits grouping
        s = re.sub(r'[\u0966-\u096F]', lambda m: str(ord(m.group(0)) - 0x0966), s)
        # If there's a range, take the lower bound
        if '-' in s:
            parts = [p.strip() for p in s.split('-') if p.strip()]
            s = parts[0]
        # remove currency symbols and letters, keep digits and separators
        s = re.sub(r"[^0-9.,]", "", s)
        # If there are multiple commas, assume Indian grouping; remove commas
        if s.count(',') > 1:
            s = s.replace(',', '')
        # Replace commas with empty and multiple dots safe-guard
        s = s.replace(',', '')
        # If blank after cleaning
        if not s:
            return 0.0
        # convert to float
        return float(s)
    except Exception:
        return 0.0


def _build_headers() -> dict:
    """Construct realistic request headers with rotating User-Agent."""
    user_agents = [
        # a small set of modern UAs
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        # minimal ch-ua hints (not guaranteed but may help some sites)
        "Sec-CH-UA": '"Chromium";v="120", "Not A;Brand";v="99"',
    }


def _requests_with_retries(url: str, headers: dict, timeout: int = 10, max_retries: int = 3, session: requests.Session | None = None) -> requests.Response | None:
    """Simple requests wrapper with retries and exponential backoff. Returns Response or None on failure."""
    sess = session or requests
    # small jitter before the request to reduce simultaneous identical requests
    time.sleep(random.uniform(0.1, 0.4))
    for attempt in range(1, max_retries + 1):
        try:
            resp = sess.get(url, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                return resp
            # If blocked (403/429/503), wait and retry
            if resp.status_code in (403, 429, 503):
                wait = 1.5 ** attempt + random.uniform(0, 0.5)
                time.sleep(wait)
                continue
            # Other statuses: return the response (caller can inspect)
            return resp
        except requests.RequestException:
            wait = 0.5 * attempt + random.uniform(0, 0.5)
            time.sleep(wait)
            continue
    return None


async def _find_most_relevant_product(query: str, products: List[Product]) -> Optional[Product]:
    """Use OpenAI to pick the most relevant product title for the user's query.

    Returns the chosen Product (falls back to first item on errors).
    """
    if not products:
        return None

    # Build numbered list of product names
    names = [p.product_name for p in products]
    numbered = "\n".join([f"{i+1}. {n}" for i, n in enumerate(names)])

    prompt = (
        f"Given the user's search for '{query}', which of the following products is the most relevant? "
        f"Respond with ONLY the index number (1-based).\n\n{numbered}\n\nIndex:" 
    )

    # Dev stub: choose the first item that contains any keyword from query or fallback to first
    if DEV_LLM_STUB:
        qwords = [w.lower() for w in re.split(r"\s+", query) if w]
        for p in products:
            name = (p.product_name or '').lower()
            if any(w in name for w in qwords):
                return p
        return products[0]

    async def _call_with_key_backoff(api_key: str, max_attempts: int = 4) -> Optional[str]:
        client = AsyncOpenAI(api_key=api_key)
        attempt = 0
        try:
            while attempt < max_attempts:
                attempt += 1
                try:
                    resp = await client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=10,
                        temperature=0.0
                    )
                    content = None
                    if resp and getattr(resp, 'choices', None):
                        choice = resp.choices[0]
                        if hasattr(choice, 'message') and getattr(choice.message, 'content', None):
                            content = choice.message.content
                        elif getattr(choice, 'text', None):
                            content = choice.text
                    return content
                except Exception:
                    wait = (1.5 ** attempt) + random.uniform(0, 0.6)
                    await asyncio.sleep(wait)
                    continue
            return None
        finally:
            if hasattr(client, 'aclose'):
                try:
                    await client.aclose()
                except Exception:
                    pass

    # Check cache first
    cached_rel = _llm_cache_get(prompt)
    if cached_rel:
        content = cached_rel
        m = re.search(r"(\d+)", content)
        if m:
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(products):
                return products[idx]

    # Try primary key first, then fallback if provided and we encounter rate limits or errors
    for key in [OPENAI_API_KEY] + ([OPENAI_API_KEY_FALLBACK] if OPENAI_API_KEY_FALLBACK else []):
        try:
            content = await _call_with_key_backoff(key)
        except Exception as e:
            # If this was a rate-limit or transient error, try next key
            continue

        if not content:
            continue

        # cache result
        try:
            _llm_cache_set(prompt, content)
        except Exception:
            pass
            pass

        m = re.search(r"(\d+)", content)
        if not m:
            continue
        idx = int(m.group(1)) - 1
        if 0 <= idx < len(products):
            return products[idx]

    # If everything failed, fall back to the first product


    return products[0]




async def search_and_recommend(query: str) -> SearchResponse:
    """Return top 2 products per platform, price summary, and prepare for Gemini AI recommendation."""
    if not query or len(query.strip()) < 2:
        raise ValueError('query must be at least 2 characters')

    browser_conf = BrowserConfig(
        headless=False,
        viewport_width=1280,
        viewport_height=720,
        verbose=True,
    )
    crawler = AsyncWebCrawler(config=browser_conf)
    try:
        amazon_task = _scrape_amazon(query, crawler)
        flipkart_task = _scrape_flipkart(query, crawler)
        results = await asyncio.gather(amazon_task, flipkart_task, return_exceptions=True)

        amazon_products = [p for p in results[0] if isinstance(p, Product)] if isinstance(results[0], list) else []
        flipkart_products = [p for p in results[1] if isinstance(p, Product)] if isinstance(results[1], list) else []

        # Enrich with local parsed data
        try:
            local_amazon = await asyncio.to_thread(_scrape_amazon_local_sync, query)
        except Exception:
            local_amazon = []
        try:
            local_flip = await asyncio.to_thread(_scrape_flipkart_local_sync, query)
        except Exception:
            local_flip = []
        amazon_products = enrich_products_with_local(amazon_products, local_amazon)
        flipkart_products = enrich_products_with_local(flipkart_products, local_flip)

        def has_all_fields(p: Product):
            return all([
                p.product_name,
                p.price is not None,
                p.rating is not None,
                p.product_url,
                p.image_url,
                p.retailer
            ])

        def select_top2(products: List[Product], query: str) -> List[Product]:
            # Filter for products with all required fields
            complete = [p for p in products if has_all_fields(p)]
            if not complete:
                return []
            # Find most relevant (highest fuzzy match)
            best = deterministic_select_most_relevant(query, complete)
            # Remove best from list, pick next best by score
            rest = [p for p in complete if p != best]
            rest_sorted = _calculate_recommendation(rest, query)
            second = rest_sorted[0] if rest_sorted else None
            result = [best] if best else []
            if second:
                result.append(second)
            return result[:2]

        top_amazon = select_top2(amazon_products, query)
        top_flipkart = select_top2(flipkart_products, query)

        def price_stats(products: List[Product]):
            prices = [p.price for p in products if p.price is not None and p.price > 0]
            if not prices:
                return None, None, None
            return min(prices), sum(prices)/len(prices), max(prices)

        all_products = top_amazon + top_flipkart
        all_prices = [p.price for p in all_products if p.price is not None and p.price > 0]
        price_low = min(all_prices) if all_prices else None
        price_avg = sum(all_prices)/len(all_prices) if all_prices else None
        price_high = max(all_prices) if all_prices else None

        ai_recommendation = None
        if all_products:
            fallback_selected = _calculate_recommendation(all_products, query)
            fallback_product = fallback_selected[0] if isinstance(fallback_selected, list) and fallback_selected else fallback_selected
            if fallback_product:
                product_name = getattr(fallback_product, 'product_name', getattr(fallback_product, 'title', 'N/A'))
                ai_recommendation = (
                    f"Best Deal: {product_name} | Price: {fallback_product.price} | Rating: {fallback_product.rating} | Retailer: {fallback_product.retailer}. "
                    "Advice: buy. Suggestion: Based on 70% price and 30% rating."
                )

        amazon_low, amazon_avg, amazon_high = price_stats(top_amazon)
        flipkart_low, flipkart_avg, flipkart_high = price_stats(top_flipkart)
        return SearchResponse(
            amazon=PlatformProducts(
                platform="Amazon",
                products=top_amazon,
                price_low=amazon_low,
                price_avg=amazon_avg,
                price_high=amazon_high,
            ),
            flipkart=PlatformProducts(
                platform="Flipkart",
                products=top_flipkart,
                price_low=flipkart_low,
                price_avg=flipkart_avg,
                price_high=flipkart_high,
            ),
            price_low=price_low,
            price_avg=price_avg,
            price_high=price_high,
            ai_recommendation=ai_recommendation
        )
    finally:
        await crawler.close()
import os
import logging
from typing import List, Optional
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel

# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configure logging
logger = logging.getLogger(__name__)

# Get SerpAPI key from environment
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
if not SERPAPI_KEY:
    logger.warning('SERPAPI_KEY not set in .env file')

class Product(BaseModel):
    product_name: str
    price: float
    rating: Optional[float] = None
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    retailer: Optional[str] = None
    final_score: Optional[float] = None
    recommendation: Optional[str] = None
    discount: Optional[str] = None

class PlatformProducts(BaseModel):
    platform: str
    products: List[Product]
    price_low: Optional[float] = None
    price_avg: Optional[float] = None
    price_high: Optional[float] = None

class SearchResponse(BaseModel):
    platforms: List[PlatformProducts]
    price_low: Optional[float] = None
    price_avg: Optional[float] = None
    price_high: Optional[float] = None
    ai_recommendation: Optional[str] = None

def extract_price(price_str) -> Optional[float]:
    """Extract numeric price from price string and convert to INR if needed"""
    if not price_str:
        return None
    
    # Convert to string if it's not already
    price_str = str(price_str)
    
    # Check if price is in USD and convert to rough INR equivalent
    if '$' in price_str and '₹' not in price_str:
        logger.debug(f"USD price detected: {price_str}, converting to INR")
        # Remove currency symbols, commas, and spaces
        import re
        price_clean = re.sub(r'[$,\s]', '', price_str)
        number_match = re.search(r'(\d+\.?\d*)', price_clean)
        if number_match:
            try:
                usd_price = float(number_match.group(1))
                # Convert USD to INR (approximate rate: 1 USD = 83 INR)
                inr_price = usd_price * 83
                logger.debug(f"Converted ${usd_price} to ₹{inr_price}")
                return inr_price
            except (ValueError, TypeError):
                return None
    
    # Handle INR prices
    import re
    price_clean = re.sub(r'[₹,\s]', '', price_str)
    
    # Extract the first number found (handles cases like "from ₹123.45")
    number_match = re.search(r'(\d+\.?\d*)', price_clean)
    if number_match:
        try:
            return float(number_match.group(1))
        except (ValueError, TypeError):
            return None
    
    return None

def extract_rating(rating_str: str) -> Optional[float]:
    """Extract numeric rating from rating string"""
    if not rating_str:
        return None
    
    import re
    rating_match = re.search(r'(\d+\.?\d*)', str(rating_str))
    if rating_match:
        try:
            return float(rating_match.group(1))
        except ValueError:
            return None
    return None

def get_retailer_from_link(link) -> str:
    """Extract retailer name from product link"""
    if not link or not isinstance(link, str):
        return "Unknown"
    
    link_lower = link.lower()
    
    # Major Indian retailers
    if 'amazon' in link_lower:
        return 'Amazon'
    elif 'flipkart' in link_lower:
        return 'Flipkart'
    elif 'croma' in link_lower:
        return 'Croma'
    elif 'reliance' in link_lower:
        return 'Reliance Digital'
    elif 'myntra' in link_lower:
        return 'Myntra'
    elif 'ajio' in link_lower:
        return 'Ajio'
    elif 'snapdeal' in link_lower:
        return 'Snapdeal'
    elif 'paytm' in link_lower:
        return 'Paytm Mall'
    elif 'jiomart' in link_lower or 'jio.com' in link_lower:
        return 'JioMart'
    elif 'bigbasket' in link_lower:
        return 'BigBasket'
    elif '93mobiles' in link_lower:
        return '93mobiles'
    elif 'nykaa' in link_lower:
        return 'Nykaa'
    elif 'tatacliq' in link_lower:
        return 'Tata CLiQ'
    elif 'shopclues' in link_lower:
        return 'ShopClues'
    elif 'limeroad' in link_lower:
        return 'LimeRoad'
    elif 'meesho' in link_lower:
        return 'Meesho'
    elif 'pepperfry' in link_lower:
        return 'Pepperfry'
    elif 'urban' in link_lower and 'ladder' in link_lower:
        return 'Urban Ladder'
    elif 'fabindia' in link_lower:
        return 'Fabindia'
    elif 'koovs' in link_lower:
        return 'Koovs'
    else:
        # Extract domain name
        from urllib.parse import urlparse
        try:
            domain = urlparse(link).netloc
            return domain.replace('www.', '').split('.')[0].title()
        except Exception:
            return "Unknown"

def calculate_recommendation_score(product: Product, all_products: List[Product]) -> Product:
    """
    Calculate recommendation score based on multiple factors:
    - Price (70% weight): Lower price = better score
    - Rating (30% weight): Higher rating = better score
    
    The score is normalized to 0-1 range and considers ALL products for comparison
    """
    if not all_products:
        product.final_score = 0.0
        product.recommendation = "Unable to compare"
        return product
    
    # Get all valid prices for comparison across ALL products
    valid_prices = [p.price for p in all_products if p.price and p.price > 0]
    if not valid_prices:
        product.final_score = 0.0
        product.recommendation = "Price not available"
        return product
    
    min_price = min(valid_prices)
    max_price = max(valid_prices)
    
    # Price score (70% weight) - lower price is better
    # Normalized to 0-1 scale where 1 = lowest price, 0 = highest price
    if product.price and product.price > 0:
        if max_price > min_price:
            price_score = (max_price - product.price) / (max_price - min_price)
        else:
            # All prices are the same
            price_score = 1.0
    else:
        price_score = 0.0
    
    # Rating score (30% weight) - higher rating is better
    # Normalized to 0-1 scale (rating out of 5)
    # If no rating, assume average (0.5)
    rating_score = (product.rating / 5.0) if product.rating else 0.5
    
    # Final score calculation (weighted average)
    # 70% price importance, 30% rating importance
    product.final_score = round((price_score * 0.7) + (rating_score * 0.3), 4)
    
    # Recommendation based on final score
    if product.final_score >= 0.8:
        product.recommendation = "Excellent Deal! Buy Now"
    elif product.final_score >= 0.6:
        product.recommendation = "Good Deal"
    elif product.final_score >= 0.4:
        product.recommendation = "Fair Price"
    else:
        product.recommendation = "Consider Waiting"
    
    logger.debug(f"Product: {product.product_name[:50]} | Price: ₹{product.price} | Rating: {product.rating} | Score: {product.final_score}")
    
    return product

async def search_google_shopping(query: str, location: str = "India", limit: int = 12) -> SearchResponse:
    """
    Search Google Shopping using SerpAPI and return structured results
    """
    if not SERPAPI_KEY:
        raise ValueError("SERPAPI_KEY not configured")
    
    # Force location to India to ensure INR pricing
    if location.lower() != "india":
        location = "India"
        logger.info("Location changed to India to ensure INR pricing")
    
    try:
        # Configure search parameters - force Indian market
        params = {
            "engine": "google_shopping",
            "q": query,
            "location": "India",  # Always use India
            "api_key": SERPAPI_KEY,
            "num": min(limit * 5, 40),  # Get more results to ensure diversity across retailers
            "hl": "en",
            "gl": "in",  # Always use Indian Google domain
            "google_domain": "google.co.in"  # Force Indian Google domain
        }
        
        logger.info(f"Searching Google Shopping for query: {query}, location: {location}")
        
        # Perform the search
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            logger.error(f"SerpAPI error: {results['error']}")
            raise ValueError(f"Search API error: {results['error']}")
        
        # Try to get inline_shopping_results first, fallback to shopping_results
        shopping_results = results.get("inline_shopping_results", [])
        if not shopping_results:
            shopping_results = results.get("shopping_results", [])
        
        if not shopping_results:
            logger.warning(f"No shopping results found for query: {query}")
            return SearchResponse(platforms=[], price_low=None, price_avg=None, price_high=None)
        
        # Process results into products
        all_products = []
        platform_groups = {}
        
        # Track retailers to ensure diversity
        amazon_products = []
        flipkart_products = []
        other_products = []
        
        for result in shopping_results[:limit * 5]:  # Get more results to ensure diversity
            try:
                logger.debug(f"Processing result: {result}")
                
                # Extract product information
                product_name = result.get("title", "Unknown Product")
                price_str = result.get("price", "")
                price = extract_price(price_str)
                
                logger.debug(f"Product: {product_name}, Price: {price}")
                
                if not price or price <= 0:
                    logger.debug(f"Skipping product due to invalid price: {price}")
                    continue  # Skip products without valid prices
                
                rating = extract_rating(result.get("rating", ""))
                
                # Handle both link formats (inline_shopping_results uses 'link', shopping_results uses 'product_link')
                product_url = result.get("link", result.get("product_link", ""))
                
                # For inline_shopping_results, prefer tracking_link if available
                if result.get("tracking_link"):
                    product_url = result.get("tracking_link")
                
                image_url = result.get("thumbnail", result.get("serpapi_thumbnail", ""))
                
                # Extract retailer from source field or fallback to URL
                retailer = result.get("source", "")
                if not retailer:
                    retailer = get_retailer_from_link(product_url)
                else:
                    # Clean up retailer names
                    retailer = retailer.replace(".in", "").replace(".com", "").strip().title()
                
                logger.debug(f"Rating: {rating}, URL: {product_url}, Retailer: {retailer}")
                
                # Extract discount if available
                discount = None
                
                # Check for old price (discount)
                if result.get("old_price") and result.get("extracted_old_price"):
                    old_price = result.get("extracted_old_price")
                    if isinstance(old_price, (int, float)) and old_price > price:
                        discount_amount = old_price - price
                        discount_percent = round((discount_amount / old_price) * 100)
                        discount = f"{discount_percent}% off (was ₹{old_price:,.0f})"
                
                # Check for installment info
                installment_info = None
                if result.get("installment"):
                    installment = result["installment"]
                    if installment.get("price") and installment.get("period"):
                        installment_info = f"{installment['price']} for {installment['period']} months"
                
                # Handle second-hand condition
                condition = result.get("second_hand_condition", "")
                if condition:
                    product_name = f"{product_name} ({condition.title()})"
                
                # Combine discount and installment info
                if installment_info and discount:
                    discount = f"{discount} | {installment_info}"
                elif installment_info:
                    discount = installment_info
                
                product = Product(
                    product_name=product_name,
                    price=price,
                    rating=rating,
                    product_url=product_url,
                    image_url=image_url,
                    retailer=retailer,
                    discount=discount
                )
                
                # Categorize products by retailer for diversity
                retailer_lower = retailer.lower()
                if 'amazon' in retailer_lower and len(amazon_products) < 2:
                    amazon_products.append(product)
                elif 'flipkart' in retailer_lower and len(flipkart_products) < 2:
                    flipkart_products.append(product)
                else:
                    # Add all other retailer products without limit at this stage
                    other_products.append(product)
                
            except Exception as e:
                logger.error(f"Error processing shopping result: {e}")
                logger.error(f"Result that caused error: {result}")
                continue
        
        # Combine products ensuring diversity (limit Amazon and Flipkart, prioritize variety)
        # First, add up to 2 from Amazon and 2 from Flipkart
        all_products = amazon_products[:2] + flipkart_products[:2]
        
        # Then add products from other retailers for diversity
        all_products.extend(other_products)
        
        # Now if we still need more products and have extras from Amazon/Flipkart, add them
        if len(all_products) < limit:
            remaining_amazon = amazon_products[2:]
            remaining_flipkart = flipkart_products[2:]
            all_products.extend(remaining_amazon + remaining_flipkart)
        
        logger.info(f"Product diversity: Amazon={len(amazon_products)}, Flipkart={len(flipkart_products)}, Others={len(other_products)}")

        
        # If we don't have enough products, add any remaining valid products
        if len(all_products) < limit:
            remaining_slots = limit - len(all_products)
            existing_urls = {p.product_url for p in all_products}
            
            # Add remaining products that weren't categorized yet
            for result in shopping_results:
                if remaining_slots <= 0:
                    break
                    
                try:
                    product_url = result.get("link", result.get("product_link", ""))
                    if result.get("tracking_link"):
                        product_url = result.get("tracking_link")
                    
                    if product_url not in existing_urls:
                        product_name = result.get("title", "Unknown Product")
                        price_str = result.get("price", "")
                        price = extract_price(price_str)
                        
                        if price and price > 0:
                            rating = extract_rating(result.get("rating", ""))
                            image_url = result.get("thumbnail", result.get("serpapi_thumbnail", ""))
                            retailer = result.get("source", "") or get_retailer_from_link(product_url)
                            retailer = retailer.replace(".in", "").replace(".com", "").strip().title()
                            
                            product = Product(
                                product_name=product_name,
                                price=price,
                                rating=rating,
                                product_url=product_url,
                                image_url=image_url,
                                retailer=retailer,
                                discount=None
                            )
                            
                            all_products.append(product)
                            existing_urls.add(product_url)
                            remaining_slots -= 1
                            
                except Exception as e:
                    logger.error(f"Error processing additional product: {e}")
                    continue
        
        all_products = all_products[:limit]  # Ensure we don't exceed limit
        
        # Ensure we have at least some Amazon and Flipkart products if available
        if not amazon_products or not flipkart_products:
            logger.warning("Missing Amazon or Flipkart products in results")
        
        if not all_products:
            logger.warning(f"No valid products found for query: {query}")
            return SearchResponse(platforms=[], price_low=None, price_avg=None, price_high=None)
        
        # Group by retailer
        platform_groups = {}
        for product in all_products:
            if product.retailer not in platform_groups:
                platform_groups[product.retailer] = []
            platform_groups[product.retailer].append(product)
        
        # Calculate recommendation scores for all products
        for product in all_products:
            calculate_recommendation_score(product, all_products)
        
        # Sort by final score (best deals first)
        all_products.sort(key=lambda x: x.final_score or 0, reverse=True)
        
        logger.info(f"Sorted {len(all_products)} products by recommendation score")
        
        # Create platform products
        platform_products = []
        for platform_name, platform_prods in platform_groups.items():
            # Sort platform products by score
            platform_prods.sort(key=lambda x: x.final_score or 0, reverse=True)
            
            # Calculate platform price statistics
            platform_prices = [p.price for p in platform_prods if p.price and p.price > 0]
            price_low = min(platform_prices) if platform_prices else None
            price_avg = sum(platform_prices) / len(platform_prices) if platform_prices else None
            price_high = max(platform_prices) if platform_prices else None
            
            platform_product = PlatformProducts(
                platform=platform_name,
                products=platform_prods,
                price_low=price_low,
                price_avg=round(price_avg, 2) if price_avg else None,
                price_high=price_high
            )
            platform_products.append(platform_product)
        
        # Sort platforms by best deal (lowest min price)
        platform_products.sort(key=lambda x: x.price_low or float('inf'))
        
        # Calculate overall price statistics
        all_prices = [p.price for p in all_products if p.price and p.price > 0]
        overall_price_low = min(all_prices) if all_prices else None
        overall_price_avg = sum(all_prices) / len(all_prices) if all_prices else None
        overall_price_high = max(all_prices) if all_prices else None
        
        # Generate AI recommendation
        ai_recommendation = generate_ai_recommendation(all_products, query)
        
        response = SearchResponse(
            platforms=platform_products,
            price_low=overall_price_low,
            price_avg=round(overall_price_avg, 2) if overall_price_avg else None,
            price_high=overall_price_high,
            ai_recommendation=ai_recommendation
        )
        
        logger.info(f"Successfully processed {len(all_products)} products across {len(platform_products)} platforms")
        return response
        
    except Exception as e:
        logger.error(f"Error in Google Shopping search: {e}")
        raise ValueError(f"Search failed: {str(e)}")

def generate_ai_recommendation(products: List[Product], query: str) -> str:
    """Generate AI recommendation based on products"""
    if not products:
        return "No products found for your search."
    
    # Find best deal
    best_product = max(products, key=lambda x: x.final_score or 0)
    
    # Count platforms
    platforms = set(p.retailer for p in products if p.retailer)
    platform_count = len(platforms)
    
    # Price range
    prices = [p.price for p in products if p.price and p.price > 0]
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        price_range = f"₹{min_price:,.0f} - ₹{max_price:,.0f}"
    else:
        price_range = "Price range not available"
    
    recommendation = f"""
🎯 **Best Deal Found**: {best_product.product_name} from {best_product.retailer}
💰 **Price**: ₹{best_product.price:,.0f}
⭐ **Rating**: {best_product.rating or 'N/A'}/5
🏆 **Recommendation**: {best_product.recommendation}

📊 **Market Overview**:
• Found {len(products)} products across {platform_count} platforms
• Price range: {price_range}
• Top platforms: {', '.join(list(platforms)[:3])}

💡 **Shopping Tip**: Compare features and delivery options before making your final decision!
    """.strip()
    
    return recommendation

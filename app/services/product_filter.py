from typing import List
from ..services.recommendation_service import Product

def is_relevant_product(product_name: str, search_query: str) -> bool:
    """
    Check if the product is relevant to the search query.
    Returns a boolean indicating whether the product should be included in results.
    """
    # Convert both to lowercase for case-insensitive comparison
    product_name = product_name.lower()
    search_query = search_query.lower()
    
    # List of keywords that indicate the product is an accessory
    accessory_keywords = [
        'case', 'cover', 'screen guard', 'screen protector', 'tempered glass',
        'charger', 'cable', 'adapter', 'skin', 'sticker', 'holder', 'mount',
        'stand', 'grip', 'earphone', 'headphone', 'earbuds', 'power bank',
        'charging pad', 'wireless charger', 'back cover', 'flip cover',
        'protective case', 'shell', 'bumper case', 'pouch', 'sleeve'
    ]
    
    # List of keywords that should be in the product name based on search query
    # Example: for "iphone 14" search, product should contain both "iphone" and "14"
    required_keywords = search_query.split()
    
    # Check if all required keywords are in the product name
    if not all(keyword.lower() in product_name for keyword in required_keywords):
        return False
    
    # Check if product name contains any accessory keywords
    for keyword in accessory_keywords:
        if keyword in product_name:
            return False
    
    return True

def filter_relevant_products(products: List[Product], search_query: str) -> List[Product]:
    """
    Return all products without filtering.
    """
    return products
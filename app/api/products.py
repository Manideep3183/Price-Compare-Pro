from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from ..services.google_shopping_service import search_google_shopping, SearchResponse

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    location: Optional[str] = "India"
    limit: Optional[int] = 12  # Increased to show more diverse products


@router.post("/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    logger.debug(f"Received search request for query: {request.query}, location: India (forced)")
    try:
        response = await search_google_shopping(
            query=request.query, 
            location="India",  # Always use India
            limit=max(10, min(request.limit or 12, 12))  # Show 10-12 products
        )
        logger.debug(f"Returning structured response for query: {request.query}")
        return response
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during search")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/locations")
async def get_supported_locations():
    """Get list of supported search locations"""
    locations = [
        {"value": "India", "label": "India"}
    ]
    return {"locations": locations}
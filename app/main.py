from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.products import router as products_router

app = FastAPI(
    title="PriceCompare Pro API",
    description="A product price comparison API using Crawl4AI and LLM strategies",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products_router, prefix="/api/v1", tags=["products"])


@app.get("/")
async def root():
    return {"message": "Welcome to PriceCompare Pro API", "version": "1.0.0"}
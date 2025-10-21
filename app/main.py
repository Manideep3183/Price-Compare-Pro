from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# API routers
from .api.products import router as products_router
from .api.activity import router as activity_router
from .db.mongo import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Close database connection
    await close_db()


app = FastAPI(
    title="SmartCart API",
    description="A product price comparison API with user authentication and activity tracking",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS - Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default dev server
        "http://localhost:8080",  # Alternative port
        "http://localhost:8081",  # Alternative port
        "http://localhost:8082",  # Alternative port
        "http://localhost:3000",  # Alternative port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "http://127.0.0.1:8082",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products_router, prefix="/api/v1", tags=["products"])
app.include_router(activity_router)  # Router already has /api/v1 prefix defined


@app.get("/")
async def root():
    return {
        "message": "Welcome to PriceCompare Pro API",
        "version": "1.0.0",
        "features": ["Product Price Comparison", "User Authentication", "Activity Tracking"]
    }
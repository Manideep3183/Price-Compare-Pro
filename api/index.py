"""
Vercel Serverless Function Entry Point
This file is the entry point for Vercel's Python serverless functions
"""
from app.main import app

# Vercel requires the ASGI app to be exposed at module level
# The variable name must match what's referenced in vercel.json
handler = app

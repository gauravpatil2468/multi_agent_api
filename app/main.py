from fastapi import FastAPI
from app.api import routes, external

app = FastAPI(
    title="Multi-Agent Backend",
    version="1.0.0",
    description="Backend for a multi-agent system using CrewAI and FastAPI, supporting client and dashboard queries, and external API interactions with MongoDB and Redis caching."
)

 # Include API routers
app.include_router(routes.router)
app.include_router(external.router, prefix="/external")

# Basic root endpoint for health check
@app.get("/", summary="Root Health Check")
async def root():
    return {"message": "Multi-Agent Backend is running!"}
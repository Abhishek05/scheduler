from typing import List
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from kids_scheduler.crews.activity_planner.activity_planner import ActivityPlanner

# Load environment variables
load_dotenv()

# Verify API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

app = FastAPI(
    title="Kids Activity Scheduler API",
    description="API for generating personalized weekly activity schedules for kids",
    version="1.0.0"
)

class ScheduleRequest(BaseModel):
    kid_age: int = Field(..., ge=6, le=16, description="Age of the kid (between 6 and 16)")
    preferred_activities: List[str] = Field(..., min_items=1, description="List of preferred activities")

class ScheduleResponse(BaseModel):
    schedule: str = Field(..., description="Generated weekly schedule in markdown format")

@app.post("/generate-schedule", response_model=ScheduleResponse)
async def generate_schedule(request: ScheduleRequest):
    """
    Generate a personalized weekly activity schedule for a kid based on their age and preferred activities.
    """
    try:
        result = (
            ActivityPlanner()
            .crew()
            .kickoff(inputs={
                "kid_age": request.kid_age,
                "preferred_activities": request.preferred_activities
            })
        )
        return ScheduleResponse(schedule=result.raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy"}

def start():
    """Entry point for running the API server"""
    import uvicorn
    uvicorn.run("kids_scheduler.api:app", host="0.0.0.0", port=8000, reload=True)
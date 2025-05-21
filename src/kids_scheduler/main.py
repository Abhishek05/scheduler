#!/usr/bin/env python
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from kids_scheduler.crews.activity_planner.activity_planner import ActivityPlanner

# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

class ActivityState(BaseModel):
    kid_age: int = 0
    preferred_activities: list[str] = []
    schedule: str = ""

class ActivityFlow(Flow[ActivityState]):
    
    @start()
    def get_user_input(self):
        print("Please enter kid's age (6-16):")
        while True:
            try:
                age = int(input())
                if 6 <= age <= 16:
                    self.state.kid_age = age
                    break
                print("Age must be between 6 and 16. Please try again:")
            except ValueError:
                print("Please enter a valid number between 6 and 16:")
        
        print("\nEnter preferred activities (one per line, press Enter twice when done):")
        activities = []
        while True:
            activity = input()
            if not activity:
                if activities:
                    break
                print("Please enter at least one activity:")
                continue
            activities.append(activity)
        self.state.preferred_activities = activities

    @listen(get_user_input)
    def generate_schedule(self):
        print("\nGenerating activity schedule...")
        result = (
            ActivityPlanner()
            .crew()
            .kickoff(inputs={
                "kid_age": self.state.kid_age,
                "preferred_activities": self.state.preferred_activities
            })
        )

        print("Schedule generated")
        self.state.schedule = result.raw

    @listen(generate_schedule)
    def save_schedule(self):
        print("Saving schedule")
        with open("schedule.md", "w") as f:
            f.write(self.state.schedule)
        print("Schedule saved to schedule.md")

def kickoff():
    activity_flow = ActivityFlow()
    activity_flow.kickoff()

def plot():
    activity_flow = ActivityFlow()
    activity_flow.plot()

if __name__ == "__main__":
    kickoff()

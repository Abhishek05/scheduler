from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class ActivityPlanner():
    """ActivityPlanner crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def curriculum_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["curriculum_planner"],
            verbose=True
        )

    @agent
    def activity_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["activity_specialist"],
            verbose=True
        )

    @agent 
    def schedule_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["schedule_optimizer"],
            verbose=True
        )

    @agent
    def progress_tracker(self) -> Agent:
        return Agent(
            config=self.agents_config["progress_tracker"],
            verbose=True
        )

    @task
    def analyze_requirements(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_requirements"]
        )

    @task
    def design_activity_pool(self) -> Task:
        return Task(
            config=self.tasks_config["design_activity_pool"]
        )

    @task
    def optimize_schedule(self) -> Task:
        return Task(
            config=self.tasks_config["optimize_schedule"]
        )

    @task
    def create_progress_metrics(self) -> Task:
        return Task(
            config=self.tasks_config["create_progress_metrics"]
        )

    @task
    def review_and_adjust(self) -> Task:
        return Task(
            config=self.tasks_config["review_and_adjust"]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ActivityPlanner crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

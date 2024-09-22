from pydantic import BaseModel
from typing import List, Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from course.tools.custom_tool import MyCustomTool

from crewai_tools import (
	ScrapeWebsiteTool,
    WebsiteSearchTool,
    SerperDevTool
)


web_rag_tool = WebsiteSearchTool()
scrape_web_tool = ScrapeWebsiteTool()
serper_tool = SerperDevTool(
    search_url="https://google.serper.dev/scholar",
    n_results=2,
)


class LearningObjective(BaseModel):
    objective: str

class TargetAudience(BaseModel):
    audience: str

class SkillLevel(BaseModel):
    level: str
    requirements: str

class Resource(BaseModel):
    description: str

class Lesson(BaseModel):
    title: str
    resources: Optional[List[Resource]] = None

class Module(BaseModel):
    title: str
    lessons: List[Lesson]
    key_concepts: List[str]
    activities: List[str]
    assessments: List[str]

class CourseOutline(BaseModel):
    title: str
    learning_objectives: List[LearningObjective]
    target_audience: List[TargetAudience]
    skill_level: SkillLevel
    modules: List[Module]
    general_resources: List[Resource]

@CrewBase
class CourseCrew():
	"""Course crew"""

	@agent
	def internet_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['internet_researcher'],
			allow_delegation=False,
			verbose=True
		)

	@agent
	def course_planner(self) -> Agent:
		return Agent(
			config=self.agents_config['course_planner'],
			allow_delegation=False,
			verbose=True
		)

	@task
	def internet_researcher_task(self) -> Task:
		return Task(
			config=self.tasks_config['internet_researcher_task'],
			tools=[web_rag_tool, serper_tool, scrape_web_tool],
		)

	@task
	def course_planner_task(self) -> Task:
		return Task(
			config=self.tasks_config['course_planner_task'],
			output_json=CourseOutline,	
			# output_file="report.json"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Course crew"""
		output = Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
		return output

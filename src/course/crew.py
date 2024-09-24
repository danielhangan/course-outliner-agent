from pydantic import BaseModel
from typing import List, Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.chat_models import ChatPerplexity
from .tools import exa_ai


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
    n_results=5,
)
exa_tools = exa_ai.search_and_get_contents_tool


class LearningObjective(BaseModel):
    objective: str

class TargetAudience(BaseModel):
    audience: str

class SkillLevel(BaseModel):
    level: str
    requirements: str

class Resource(BaseModel):
    description: str
    url: str

class GeneralResource(BaseModel):
    title: str
    url: str

class YoutubeResource(BaseModel):
    title: str
    url: str


class ReadingResource(BaseModel):
    title: str
    url: str

class Lesson(BaseModel):
    title: str
    resources: List[Resource]

class Module(BaseModel):
    title: str
    lessons: List[Lesson]
    key_concepts: List[str]
    activities: List[str]
    assessments: List[str]


class ExpectedOutcome(BaseModel):
    outcome: str


class CourseOutline(BaseModel):
    title: str
    description: str
    learning_objectives: List[LearningObjective]
    target_audience: List[TargetAudience]
    expected_outcome: List[ExpectedOutcome]
    skill_level: SkillLevel
    modules: List[Module]
    general_resources: List[GeneralResource]
    relevant_youtube_videos: List[YoutubeResource]
    relevant_readings: List[ReadingResource]

@CrewBase
class CourseCrew():
	"""Course crew"""

	@agent
	def course_designer(self) -> Agent:
		return Agent(
			config=self.agents_config['course_designer'],
			allow_delegation=False,
			verbose=True
		)

	@agent
	def internet_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['internet_researcher'],
			allow_delegation=False,
			tools=[exa_tools],
			verbose=True
		)

	@agent
	def course_planner(self) -> Agent:
		return Agent(
			config=self.agents_config['course_planner'],
			verbose=True
		)

  
	@task
	def course_design_task(self) -> Task:
		return Task(
			config=self.tasks_config['course_design_task'],
			# tools=[web_rag_tool],
		)

	@task
	def internet_researcher_task(self) -> Task:
		return Task(
			config=self.tasks_config['internet_researcher_task'],
			tools=[scrape_web_tool],
		)

	@task
	def relevant_youtube_videos_task(self) -> Task:
		return Task(
			config=self.tasks_config['relevant_youtube_videos_task'],
			tools=[exa_tools]
		)

	@task
	def relevant_reading_list_task(self) -> Task:
		return Task(
			config=self.tasks_config['relevant_reading_list_task'],
			tools=[exa_tools]
		)

	@task
	def course_planner_task(self) -> Task:
		return Task(
			config=self.tasks_config['course_planner_task'],
			output_json=CourseOutline,	
			output_file="report.json"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Course crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

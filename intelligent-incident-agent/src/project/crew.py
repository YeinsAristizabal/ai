# src/project/crew.py
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = LLM(
    model="groq/llama3-8b-8192",
    temperature=0.3,
    base_url="https://api.groq.com/openai/v1"
)

# llm = LLM(model="ollama/gemma:2b", base_url="http://localhost:11434")

@CrewBase
class incidentHandling():
	"""LatestAiDevelopment crew"""
	# agents_config_path = 'config/agents.yaml'
	# tasks_config_path  = 'config/tasks.yaml'

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def detect_category(self) -> Agent:
		return Agent(
			config=self.agents_config['detect_category'],
			llm=llm
		)

	@agent
	def detect_area(self) -> Agent:
		return Agent(
			config=self.agents_config['detect_area'],
			llm=llm
		)

	@agent
	def sentiment_analysis(self) -> Agent:
		return Agent(
			config=self.agents_config['sentiment_analysis'],
			llm=llm
		)

	@task
	def _detect_category(self) -> Task:
		return Task(
			config=self.tasks_config['_detect_category'],
			agent = self.detect_category(),
		)

	@task
	def _detect_area(self) -> Task:
		return Task(
			config=self.tasks_config['_detect_area'],
			agent = self.detect_area(),
		)
	
	@task
	def _sentiment_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['_sentiment_analysis'],
			agent = self.sentiment_analysis(),
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the incidentHandling crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			# verbose=True,
		)
from crewai import Agent, Crew, Process, Task , LLM
from crewai.project import CrewBase, agent, crew, task 
from signon_crew.tools import Fetch_vessel,crew_onboard ,crew_replace
from signon_crew.tools.crew_onboard	import FetchCrewOnboard
from signon_crew.tools.crew_replace	import FetchCrewRep
from signon_crew.tools.Fetch_vessel	import FetchVesselPosition

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SignonCrew():
	"""SignonCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def vessl_pos_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['vessl_pos_agent'],
			llm=LLM(model="azure/gpt-4o-2024-11-20"),
			verbose=True
		)

	@agent
	def crew_on_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['crew_on_agent'],
			tools=[FetchCrewOnboard()],
			llm=LLM(model="azure/gpt-4o-2024-11-20"),
			verbose=True
		)
	
	@agent
	def crew_replace_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['crew_replace_agent'],
			tools=[FetchCrewRep()],
			llm=LLM(model="azure/gpt-4o-2024-11-20"),
			verbose=True
		)
	
	@agent
	def Summarizer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['Summarizer_agent'],
			llm=LLM(model="azure/gpt-4o-2024-11-20"),
			verbose=True
		)


	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def vessel_find(self) -> Task:
		return Task(
			config=self.tasks_config['vessel_find'],
			tools=[FetchVesselPosition()] ,
		)

	@task
	def crew_onboard_task(self) -> Task:
		return Task(
			config=self.tasks_config['crew_onboard_task'],
			tools=[FetchCrewOnboard()] ,
			async_execution=False
		)
	
	@task
	def find_replacement_task(self) -> Task:
		return Task(
			config=self.tasks_config['find_replacement_task'],
			tools=[FetchCrewRep()] ,
			llm =LLM(model="azure/gpt-4o-2024-11-20"),
			async_execution=False
		)
	
	@task
	def summary_task(self) -> Task:
		return Task(
			config=self.tasks_config['summary_task'],
			async_execution=False
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SignonCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			#manager_llm=LLM(model="azure/gpt-4o-2024-11-20"),
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

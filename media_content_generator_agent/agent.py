from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from transcription_reader_tools import list_available_creators, get_creator_transcriptions

from dotenv import load_dotenv
load_dotenv()

# Setup DB
db = SqliteDb(db_file="tmp/data.db")

# Setup Agents
copywriter = Agent(
    model=OpenAIChat(id="gpt-5-nano"),
    name="copywriter",
    description="",

    add_history_to_context=True,
    num_history_runs=3,

    tools=[TavilyTools(), list_available_creators, get_creator_transcriptions],
    db = db,
    instructions=open("prompts/copywriter.md").read()
)

# Setup AgentOs

agent_os = AgentOS(
    name="agent_os",
    description="",
    agents=[copywriter]
    )

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agent:app", reload=True)
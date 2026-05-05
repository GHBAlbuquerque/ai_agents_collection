# =============================================================================
# N1 - News Curator Agent (Level 1: single agent with external reusable skills)
# =============================================================================
#
# This script creates a SINGLE AI AGENT that acts as a complete journalist.
# It receives a topic and executes the entire pipeline on its own:
#
#    TOPIC → Research → Investigation → Verification → Writing → Final Article (.md)
#
# Skills are organized in external files in the `/skills` folder and imported here.
# =============================================================================

from pathlib import Path
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools
from agno.tools.file import FileTools
from agno.skills import Skills, LocalSkills

import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------
# 1. TOOLS CONFIGURATION
#   Filetools is used to:
#   - save file in .md
#   - read existing files
#   - list files in output dir
# ------------------------------------------

# Path to skill .md (or .txt) files
skills_dir = Path(__file__).parent/"skills"

# Path to output results from news search
output_dir = Path(__file__).parent/"output/N1"

file_tools = FileTools(
    base_dir=output_dir,
    enable_save_file=True,
    enable_read_file=True,
    enable_list_files=True
)


# ------------------------------------------
# 2. AGENT INITILIZATION
#   Create agent with
#   - name
#   - model
#   - instructions
#   - tools
# ------------------------------------------

news_agent = Agent(
    name="News Agent",
    model=OpenAIResponses(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    skills=Skills(loaders=[LocalSkills(str(skills_dir))]),
    instructions=[
        "You are a complete journalist: researcher, investigator, fact-checker, and writer.",
        "Receive a topic and execute ALL the steps below in sequence.",
        "",
        "STEP 1 - NEWS SEARCH: use the 'news-search' skill",
        "STEP 2 - SOURCE VERIFICATION: use the 'source-verification' skill",
        "STEP 3 - FACT CHECKING: use the 'fact-checking' skill",
        "STEP 4 - JOURNALISTIC WRITING: use the 'journalistic-writing' skill",
        "",
        "Present ONLY the final news article (Step 4) to the user.",
        "Steps 1, 2, and 3 are your internal workflow.",
        "Save the final document as a .md file in the directory",
    ],
    tools=[WebSearchTools(), file_tools],
    add_datetime_to_context=True,
    markdown=True,
    #debug_mode=True
)

# ------------------------------------------
# 3. AGENT EXECUTION
#   Agent gets a topic and executes the pipeline
#   print_response() shows the anseer on the terminal
# ------------------------------------------

if __name__ == "__main__":
    news_agent.print_response(
        "Bank of America believes GTA 6 will cost $80 and introduce new base price for games",
        stream=True # streams each step
    )
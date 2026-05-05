# =============================================================================
# N0 - News Curator Agent (Level 0: single agent)
# =============================================================================
#
# This script creates a SINGLE AI AGENT that acts as a complete journalist.
# It receives a topic and executes the entire pipeline on its own:
#
#    TOPIC → Research → Investigation → Verification → Writing → Final Article (.md)
# =============================================================================

from pathlib import Path
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools
from agno.tools.file import FileTools
from skills.N0_dictionary_news_skills import NEWS_AGENT_SKILLS

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

# Path to output results from news search
output_dir = Path(__file__).parent/"output/N0"

file_tools = FileTools(
    base_dir=output_dir,
    enable_save_file=True,
    enable_read_file=True,
    enable_list_files=True
)

# ------------------------------------------
# 2. SKILLS
#   Inject on prompt via prompt instructions
#   - Input: expected input
#   - Process: step-by-step
#   - Output format: how the output should be
#   - Rules: guidelines that should be followed 
# ------------------------------------------

prompt_instructions = "\n\n".join(NEWS_AGENT_SKILLS.values())

# ------------------------------------------
# 3. AGENT INITILIZATION
#   Create agent with
#   - name
#   - model
#   - instructions
#   - tools
# ------------------------------------------

news_agent = Agent(
    name="News Agent",
    model=OpenAIResponses(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    instructions=[
        "You are a complete journalist: researcher, investigator, fact-checker, and writer.",
        "Receive a topic and execute ALL the steps below in sequence.",
        "",
        "Strictly follow the instructions for each stage defined in the skills below:",
        prompt_instructions,
        "",
        "STEP 1 - NEWS SEARCH: execute the 'NEWS SEARCH' instructions",
        "STEP 2 - SOURCE VERIFICATION: execute the 'JOURNALISTIC SOURCE INVESTIGATION' instructions",
        "STEP 3 - FACT CHECKING: execute the 'FACT CHECKING' instructions",
        "STEP 4 - WRITING: execute the 'JOURNALISTIC NEWS WRITING' instructions",
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
# 4. AGENT EXECUTION
#   Agent gets a topic and executes the pipeline
#   print_response() shows the anseer on the terminal
# ------------------------------------------

if __name__ == "__main__":
    news_agent.print_response(
        "Spotify adds 'Verified' badges to distinguish human artists from AI"
    )
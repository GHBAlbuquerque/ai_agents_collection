# =============================================================================
# N2 - News Curator Agent (Level 2: agents workflow)
# =============================================================================
#
# This script creates a WORKFLOW OF AI AGENTS that acts as a complete journalist.
# It receives a topic and executes the entire pipeline on its own:
#
#    TOPIC → Research → Investigation → Verification → Writing → Final Article (.md)
#
# Skills are organized in external files in the `/skills` folder and imported here.
# Workflow used to make agents work as a "team of specialists"
# =============================================================================

from pathlib import Path
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools
from agno.tools.file import FileTools
from agno.skills import Skills, LocalSkills
from agno.workflow import Workflow

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

shared_skills = Skills(loaders=[LocalSkills(str(skills_dir))])

# Path to output results from news search
output_dir = Path(__file__).parent/"output/N1"

file_tools = FileTools(
    base_dir=output_dir,
    enable_save_file=True,
    enable_read_file=True,
    enable_list_files=True
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. CREATING SPECIALIST AGENTS
#    We create 4 agents, each with a specific "role."
#    They use the same 'shared_skills', but receive focused instructions.
# ─────────────────────────────────────────────────────────────────────────────

# 1) Researcher - uses the news search skill
researcher = Agent(
    name="Researcher",
    model=OpenAIResponses(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    skills=shared_skills,
    instructions=[
        "You are a news researcher.",
        "Before starting, load the skill instructions using get_skill_instructions.",
        "Execute the 'news-search' skill and return exactly in the format defined within it.",
        "Save the research result to a file using the file tool.",
    ],
    tools=[WebSearchTools(), file_tools],
    add_datetime_to_context=True,
    markdown=True,
)

# 2) Source Auditor - uses the multi-source verification skill
source_auditor = Agent(
    name="Source Auditor",
    model=OpenAIResponses(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    skills=shared_skills,
    instructions=[
        "You are a journalistic source auditor.",
        "Before starting, load the skill instructions using get_skill_instructions.",
        "Receive the output from the researcher and execute the 'source-verification' skill.",
        "Save the verification result to a file using the file tool.",
    ],
    tools=[WebSearchTools(), file_tools],
    add_datetime_to_context=True,
    markdown=True,
)

# 3) Fact-Checker - uses the fact-checking skill
fact_checker = Agent(
    name="Fact-Checker",
    model=OpenAIResponses(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    skills=shared_skills,
    instructions=[
        "You are a fact-checker.",
        "Before starting, load the skill instructions using get_skill_instructions.",
        "Receive the dossier from the auditor and execute the 'fact-checking' skill.",
        "Save the verification result to a file using the file tool.",
    ],
    tools=[WebSearchTools(), file_tools],
    add_datetime_to_context=True,
    markdown=True,
)

# 4) Writer - uses the journalistic writing skill
writer = Agent(
    name="Writer",
    model=OpenAIResponses(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    skills=shared_skills,
    instructions=[
        "You are a professional journalistic writer.",
        "Before starting, load the skill instructions using get_skill_instructions.",
        "Receive the report from the fact-checker and execute the 'journalistic-writing' skill.",
        "IMPORTANT: When citing any data, fact, or information from a source, insert numerical references [1], [2], [3], etc., in the body of the text.",
        "IMPORTANT: At the end of the article, include a '## References' section with a numbered list of all sources, including the media outlet name, title, and full URL.",
        "Upon finishing the writing, save the content to a file using the file tool.",
    ],
    tools=[file_tools],
    markdown=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. WORKFLOW DEFINITION
#    Workflow connects the agents in a logical sequence.
#    The output of an agent is passed down to the next as its input. 
#
#    TOPIC → Research → Investigation → Verification → Writing → Final Article (.md)
# ─────────────────────────────────────────────────────────────────────────────

workflow = Workflow(
    name="News Curator with Workflow",
    description="Researches, investigates, verifies and writes articles",
    steps=[researcher, source_auditor, fact_checker, writer]
)

# ------------------------------------------
# 4.EXECUTION
#   Workflow gets a topic and executes the pipeline
#   print_response() shows the anseer on the terminal
# ------------------------------------------

if __name__ == "__main__":
    Workflow.print_response(
        self=workflow,
        input="Egg freezing popularity increasing among young women to preserve their fertility",
        stream=True, # streams each step
        markdown=True
    )
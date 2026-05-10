# =============================================================================
# N2 - News Curator Agent (Level 2: agents workflow)
# =============================================================================
#
# This script creates a WORKFLOW OF AI AGENTS that acts as a complete journalist.
# It receives a topic and executes the entire pipeline on its own:
#
#    TOPIC → Research → Investigation (loop) → Verification → Writing → Final Article (.md)
#
# Skills are organized in external files in the `/skills` folder and imported here.
# Workflow used to make agents work as a "team of specialists"
# =============================================================================

from typing import List

from pathlib import Path
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools
from agno.tools.file import FileTools
from agno.skills import Skills, LocalSkills
from agno.workflow import Step, Loop, Workflow
from agno.workflow.types import StepOutput

import re #regex lib
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------
# 1. GLOBAL VARIABLES DEFINITION
# ------------------------------------------
MIN_SOURCES = 3
MAX_VERIFICATION_RETRY = 3

# ------------------------------------------
# 2. TOOLS CONFIGURATION
#   Filetools is used to:
#   - save file in .md
#   - read existing files
#   - list files in output dir
# ------------------------------------------

# Path to skill .md (or .txt) files
skills_dir = Path(__file__).parent/"skills"

shared_skills = Skills(loaders=[LocalSkills(str(skills_dir))])

# Path to output results from news search
output_dir = Path(__file__).parent/"output/N3"

file_tools = FileTools(
    base_dir=output_dir,
    enable_save_file=True,
    enable_read_file=True,
    enable_list_files=True
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. CREATING SPECIALIST AGENTS
#    We create 4 agents, each with a specific "role."
#.   And one Team to coordinate the research step.
#    They use the same 'shared_skills', but receive focused instructions.
# ─────────────────────────────────────────────────────────────────────────────

# 1.1) Researcher - uses the news search skill
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

# 1.2) Research team
# the team leads and coordinates the agent
research_team = Team(
    name="Research Team",
    model=OpenAIResponses(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    members=[researcher],
    instructions=[
        "You are the research team leader.",
        "Your mission is to coordinate the search for relevant and recent news on the requested topic.",
        "Ensure that the researcher uses the 'news-search' skill correctly.",
        "The ultimate goal is to provide a rich set of information for the subsequent investigation and verification stages.",
        "Make sure that the results are correctly saved to a file.",
    ],
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
        f"IMPORTANT: You MUST find at least {MIN_SOURCES} distinct sources.",
        "For each source, ALWAYS include the outlet name in bold and the full URL.",
        "Use the format: - **Outlet Name**: Article title (URL)",
        "If the previous verification did not reach the minimum, search for sources DIFFERENT from those already found.",
        "Try other outlets, international agencies (Reuters, AP, AFP), and various portals.",
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
        "Receive the verifier's report and execute the 'journalistic-writing' skill.",
        f"If the report indicates fewer than {MIN_SOURCES} independent sources, include a clear warning at the beginning of the article: '⚠️ NOTE: This article was produced with a limited number of independent sources.'",
        "IMPORTANT: When citing any data, fact, or information from a source, insert a numerical reference [1], [2], [3] etc. in the body of the text.",
        "IMPORTANT: At the end of the article, include a '## References' section with a numbered list of all sources, including the outlet name, title, and full URL.",
        "MANDATORY: Upon finishing the writing process, you MUST save the complete article in a Markdown (.md) file using the save_file tool.",
        "Use the filename format: article_<summarized_topic>_<date_YYYY-MM-DD>.md (e.g., article_brazilian_economy_2026-02-10.md).",
        "Never finish without saving the file. Confirm the name of the saved file in your final response.",
    ],
    tools=[file_tools],
    markdown=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 4. AUXILIARY FUNCTIONS AND LOOP CONDITIONS
#    1. An evaluation metric (count_sources function) that tells if the response was good.
#    2. A stop condition (sufficient_sources function) that the Loop checks 
#       at each iteration. If the condition is met, the Loop ends; 
#       otherwise, it finishes if we reach MAX_VERIFICATION_ATTEMPTS.
# ─────────────────────────────────────────────────────────────────────────────

def count_sources(text: str) -> int:
    """
    Auxiliary Function: Analytical extraction and counting
    
    Analyzes the text returned by the Research Agent to count the number
    of distinct sources it managed to find. To ensure we are not 
    counting repeated sources just by the section title, we use 
    Regular Expressions (Regex) to scan the text.
    
    How it works:
    1. Isolates the specific section ("COLLECTED SOURCES") from the dossier.
    2. Counts how many Markdown-formatted items (e.g., "- **Outlet**") exist.
    3. Counts how many distinct web links (URLs or http/https) exist in the text.
    4. Returns the higher number between the two counts (ensuring the worst-case scenario).
    """
    section = text
    
    # Step 1: Captures the specific content of COLLECTED SOURCES via Regex
    # `re.search`: looks for the first occurrence.
    # Pattern: Looks for "## COLLECTED SOURCES" (with optional spaces \s*), captures everything (.*?)
    #          lazily until it finds the next "##" or the end of the text (##|$).
    # `re.DOTALL`: Makes the `.` also capture line breaks (\n).
    # `re.IGNORECASE`: Ignores uppercase/lowercase.
    # `match.group(1)`: Takes only the captured content, ignoring the headers.
    match = re.search(
        r"##\s*COLLECTED SOURCES(.*?)(##|$)", text, re.DOTALL | re.IGNORECASE
    )
    if match:
        section = match.group(1)

    # Step 2: Search for Markdown-formatted source lists via Regex
    # `re.findall`: finds all occurrences.
    # Pattern `r"^-\s+\*\*"`: Looks for the start of the line ^, hyphen -, one or more spaces \s+ 
    #                        and two literal asterisks \*\* (indicating bold in markdown).
    # `re.MULTILINE`: Treats each new line as a new start for ^.
    sources_by_bullet = re.findall(r"^-\s+\*\*", section, re.MULTILINE)
    
    # Step 3: Extract and create a grouping of unique values (set) of the URLs 
    # found in the text to quickly discard repeated links.
    # Pattern `r"https?://[^\s\)]+"`: Looks for links starting with "http://" or "https://", 
    #                                followed by 1 or more characters that are NOT whitespace 
    #                                nor closing parentheses (common in Markdown).
    # `set(...)`: Creates a set to automatically eliminate duplicate URLs.
    urls = set(re.findall(r"https?://[^\s\)]+", section))

    # We return the maximum number captured, as some links might not have the bullet point,
    # or the bullet points might not contain links. The higher balance validates a sensible count.
    return max(len(sources_by_bullet), len(urls))


def sufficient_sources(outputs: List[StepOutput]) -> bool:
    """
    Stop Condition Function (End Condition): Validating the Loop
    
    Used as an instruction in the research loop stage (research_loop).
    This function evaluates the last response (outputs[-1]) obtained and validates
    if it meets our newsroom's business rule: reaching a predetermined 
    minimum number of sources.
    
    Workflow in practice:
    - The research Loop executes its task using the corresponding agent.
    - This condition (sufficient_sources) is executed next externally, 
      injecting the execution 'outputs'.
    - If it returns 'True', the agent met the goal and proceeds to Fact-Checking.
    - If it returns 'False', the research stage repeats.

    Args:
        outputs (List[StepOutput]): History of responses/steps from the previous Workflow.
    Returns:
        bool: Returns True if it reached or exceeded MIN_SOURCES, otherwise False.
    """
    if not outputs:
        # If for some reason there is no output from the previous agent, we request a new iteration.
        return False
        
    # Extract the response obtained by the agent's most recent iteration (index [-1])
    latest = outputs[-1]
    
    # Extract the plain text content generated by this agent request
    content = str(latest.content or "")
    
    # Finally, we pass the final text through the previous analytical function that performs the
    # count. We compare the result using the static constant (MIN_SOURCES) from the top.
    return count_sources(content) >= MIN_SOURCES

# ─────────────────────────────────────────────────────────────────────────────
# 5. STEPS AND LOOP DEFINITION
#    Instead of agents, workflow now gets STEPS.
#    Each step gets an agent and can be retried/run in loop if desired.
#
#    TOPIC → Research → Investigation (loop) → Verification → Writing → Final Article (.md)
# ─────────────────────────────────────────────────────────────────────────────

# Step 1 - Research
research_step = Step(
    name="research",
    description="Searches for news with the desired subject",
    team=research_team
)

# Step 2 - Verification
source_verification_step = Step(
    name="source_verification",
    description="multi-source verification",
    agent=source_auditor
)

# Step 2 (Loop) - loops until enough sources are found
source_verification_loop = Loop(
    name="source_verification_loop",
    description="Repeats verification until enough sources are found",
    steps=[source_verification_step],
    max_iterations=MAX_VERIFICATION_RETRY,
    end_condition=sufficient_sources
)

# Step 3 - Fact Checking
fact_checking_step = Step(
    name="fact-checking",
    description="dossier fact checking",
    agent=fact_checker
)

# Step 4 - Journalistic Writing
journalistic_writing_step = Step(
    name="journalistic_writing",
    description="Writes final version o news article",
    agent=writer
)

# ─────────────────────────────────────────────────────────────────────────────
# 6. WORKFLOW DEFINITION
#    Workflow connects the agents in a logical sequence.
#    The output of an agent is passed down to the next as its input. 
#
#    TOPIC → Research → Investigation → Verification → Writing → Final Article (.md)
# ─────────────────────────────────────────────────────────────────────────────

workflow = Workflow(
    name="News Curator with Workflow",
    description="Researches, investigates, verifies and writes articles",
    steps=[research_step, source_verification_loop, fact_checking_step, journalistic_writing_step]
)

# ------------------------------------------
# 7.EXECUTION
#   Workflow gets a topic and executes the pipeline
#   print_response() shows the anseer on the terminal
# ------------------------------------------

if __name__ == "__main__":
    Workflow.print_response(
        self=workflow,
        input="Katseye's Manon to Take 'Temporary Hiatus from Group Activities'",
        stream=True, # streams each step
        markdown=True
    )
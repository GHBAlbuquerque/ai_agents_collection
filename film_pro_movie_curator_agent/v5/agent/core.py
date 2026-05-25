from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools

from agent.config import Config
from agent.models import MovieRecommendation
from agent.prompts import description, instructions
from agent.tools.omdb import search_movie

import dotenv

dotenv.load_dotenv(dotenv_path=".env", override=True)

movie_recommendation_agent = Agent(
    name="FilmPro",
    model=OpenAIChat(id="gpt-5-nano", api_key=Config.get_openai_key()),
    tools=[WebSearchTools(), search_movie],
    description=description,
    instructions=instructions,
    add_datetime_to_context=True,
    markdown=True,
    output_schema=MovieRecommendation,
    debug_mode=True,
    debug_level=1
)

async def get_recommendations(input: str) -> MovieRecommendation:
    result = await movie_recommendation_agent.arun(
        input,
        stream=False
    )
    
    if not result or not result.content:
        raise Exception("Error trying to obtain recommendations.")
    
    
    data: MovieRecommendation = result.content
    pretty_json_output = data.model_dump_json(
        indent=2,
    )
    
    print(pretty_json_output)
    
    return data
    
    
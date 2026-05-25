import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools

from config import Config
from models import MovieRecommendation
from prompts import description, instructions
from tools.omdb import search_movie

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

async def recommendations():
    result = await movie_recommendation_agent.arun(
        "I'm looking for fictional movies set in the music world, similar in tone or subject to Rock Star (2001).",
        stream=False
    )
    
    if result and result.content:
        data: MovieRecommendation = result.content
        pretty_json_output = data.model_dump_json(
            indent=2,
        )
        
        print(pretty_json_output)
        
        return result
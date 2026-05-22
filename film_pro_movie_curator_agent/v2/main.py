import asyncio

from prompts import description, instructions
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools

from models import MovieRecommendation

import os
import dotenv
dotenv.load_dotenv(dotenv_path=".env", override=True)

movie_recommendation_agent = Agent(
    name="FilmPro",
    model=OpenAIChat(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[WebSearchTools()],
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
        "I loved 'Legally Blonde' because of the 'underestimated blonde' trope and the fish-out-of-water setting."
        "Can you recommend 5 similar movies with an IMDb rating above 7.5? I'm looking for something uplifting with a strong female lead.",
        stream=False
    )
    
    if result and result.content:
        data: MovieRecommendation = result.content
        pretty_json_output = data.model_dump_json(
            indent=2,
        )
        
        print(pretty_json_output)
        
        return result

if __name__ == "__main__":
    asyncio.run(recommendations())
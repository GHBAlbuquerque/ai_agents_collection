from prompts import description, instructions
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools

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
    markdown=True
)

if __name__ == "__main__":
    movie_recommendation_agent.print_response(
        input="I loved 'Legally Blonde' because of the 'underestimated blonde' trope and the fish-out-of-water setting. Can you recommend 5 similar movies with an IMDb rating above 7.5? I'm looking for something uplifting with a strong female lead.",
        stream=True
    )
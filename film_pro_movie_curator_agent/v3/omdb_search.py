from typing import Any

import aiohttp

import os
import dotenv
dotenv.load_dotenv(dotenv_path=".env", override=True)

#http://www.omdbapi.com/?i=tt3896198&apikey=729906d
async def search_movie(title: str) -> dict[str, Any] | str:
     api_key=os.getenv("OMDB_API_KEY")
     
     if not api_key:
         raise ValueError("OMDB_API_KEY not configured")
     
     async with aiohttp.ClientSession() as session:
         try: 
             async with session.get(
                 "http://www.omdbapi.com/",
                 params={
                     "apikey": api_key,
                     "t": title,
                     "type": "movie", # brings only movies results
                     "plot": "full", # full plot return
                     "v": "1" # api version
                 },
                 timeout=aiohttp.ClientTimeout(total=10) # 10s timeout
             ) as response:
                if response.status != 200:
                    return f"Error when searching for movie: Status {response.status}"

                data = await response.json()

                if data.get("Response" == "False"):
                    return f"Movie not found: {title}"

                return data     
         except Exception as e:
            return f"Error when searching for movie: {e}"
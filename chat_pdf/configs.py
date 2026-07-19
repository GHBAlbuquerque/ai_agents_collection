from pathlib import Path

FILES_FOLDER = Path(__file__).parent / 'files'
RETRIEVAL_SEARCH_TYPE = 'mmr'
RETRIEVAL_ARGS = {"k":2, "fetch_k": 10}
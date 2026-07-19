from pathlib import Path
import streamlit as st
from prompts import SYSTEM_PROMPT

FILES_FOLDER = Path(__file__).parent / 'files'
MODEL_NAME = "gpt-5.4-mini"
RETRIEVAL_SEARCH_TYPE = 'mmr'
RETRIEVAL_ARGS = {"k":2, "fetch_k": 10}
PROMPT = SYSTEM_PROMPT

def get_config(config_name: str):
    config_name_lc = config_name.lower()
    config_getters = {
        'model_name': get_model_name,
        'retrieval_search_type': get_retrieval_search_type,
        'retrieval_args': get_retrieval_args,
        'prompt': get_system_prompt
    }
    config_getter = config_getters.get(config_name_lc) # get function
    if config_getter:
        return config_getter(config_name_lc) # execute function

def get_model_name(model_name: str):
    if model_name in st.session_state:
        return st.session_state[model_name]
    return MODEL_NAME

def get_retrieval_search_type(retrieval_search_type: str):
    if retrieval_search_type in st.session_state:
        return st.session_state[retrieval_search_type]
    return RETRIEVAL_SEARCH_TYPE

def get_retrieval_args(retrieval_args: str):
    if retrieval_args in st.session_state:
        return st.session_state[retrieval_args]
    return RETRIEVAL_ARGS

def get_system_prompt(prompt: str):
    if prompt in st.session_state:
        return st.session_state[prompt]
    return PROMPT


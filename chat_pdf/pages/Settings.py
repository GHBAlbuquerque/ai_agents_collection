import streamlit as st
from configs import get_config
import json

def settings_page():
    st.header('Settings', divider=True)
    
    model_name = st.text_input('Modify model', value=get_config('model_name'))
    retrieval_search_type = st.text_input('Modify search type', value=get_config('retrieval_search_type'))
    retrieval_args = st.text_input('Modify search args', value=json.dumps(get_config('retrieval_args')))
    prompt = st.text_area('Modify prompt', height=350, value=get_config('prompt'))
    
    if st.button('Modify settings', use_container_width=True):
        retrieval_args_json = json.loads(retrieval_args)
        
        st.session_state['model_name'] = model_name
        st.session_state['retrieval_search_type'] = retrieval_search_type
        st.session_state['retrieval_args'] = retrieval_args_json
        st.session_state['prompt'] = prompt

settings_page()
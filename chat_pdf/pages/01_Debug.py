import json
import streamlit as st
from prompts import SYSTEM_PROMPT, HUMAN_PROMPT
from ingestion import create_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def format_docs_output(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def debug_page():
    st.header('Debug page', divider=True)
    
    memory = st.session_state.get('memory', None)
    history = memory.messages if memory else []
    retriever = create_retriever()
    mock_question = "Placeholder question for debugging"
    retrieved_docs = retriever.invoke(mock_question) # invoke retriever to get actual chunks

    actual_context_string = format_docs_output(retrieved_docs)
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", HUMAN_PROMPT)
    ])
    
    # string interpolation to build and prepare the prompt
    formatted_prompt = prompt_template.format_messages(
        history = history,
        context = actual_context_string,
        question = "Placeholder question for debugging"
    )
    
    messages_dict = [msg.model_dump() for msg in formatted_prompt]
    
    json_string = json.dumps(messages_dict, indent=2)
    
    with st.container(border=True):
        st.code(json_string, language="json", wrap_lines=True)
    
debug_page()
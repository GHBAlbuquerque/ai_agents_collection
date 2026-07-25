import streamlit as st

from ingestion import create_retriever
from agent import create_chain_and_memory

def init():
    if 'chain' not in st.session_state or 'memory' not in st.session_state:
        with st.spinner("Initializing Vector Database..."):
            retriever = create_retriever()
            chain, memory = create_chain_and_memory(retriever)
            
            st.session_state['memory'] = memory
            st.session_state['chain'] = chain


def chat_window():
    
    st.markdown(
    "<h2 style='text-align: center;'> Welcome to RO Character Lore Generator</h2>",
    unsafe_allow_html=True
    )
     
    chain = st.session_state['chain']
    memory = st.session_state['memory']
    history = memory.messages
    
    container = st.container()
    for message in history:
        chat = container.chat_message(message.type)
        chat.markdown(message.content)
        
    input = st.chat_input("Ask me anything!")
    if input:
        memory.add_user_message(input)
        
        chat = container.chat_message('human')
        chat.markdown(input)
        
        chat = container.chat_message('ai')
        chat.markdown("Generating answer...")

        answer = chain.invoke(input)
        formatted_answer = answer.replace('\n', '\n\n')
        
        memory.add_ai_message(formatted_answer)
        st.rerun()

def main():
    init()
    chat_window()
    
if __name__ == "__main__":
    main()



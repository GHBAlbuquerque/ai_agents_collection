from pathlib import Path
from langchain_core.chat_history import InMemoryChatMessageHistory
import streamlit as st
from configs import FILES_FOLDER
from ingestion import create_retriever
from agent import create_chain_and_memory

"""
Owns StreamLit components and Session State.
Calls ingestion for document upload and Retriever creation.
Uses Chain and Memory from agent on chat.
"""

def sidebar():
    uploaded_pdfs = st.file_uploader("Add your PDF files:", type=['.pdf'], accept_multiple_files=True)
    
    if uploaded_pdfs is None:
        return
    
    for file in FILES_FOLDER.glob('*.pdf'):
        file.unlink() # deletes all previously saved files
        
    for pdf in uploaded_pdfs:
        with open(FILES_FOLDER / pdf.name, 'wb') as f: #open file to save and web = write bytes
            f.write(pdf.read())

    label_button = 'Start ChatBot'
    if 'chain' in st.session_state:
        label_button = 'Refresh ChatBot'
    
    if st.button(label_button, use_container_width=True, type='primary'):
        if len(list(FILES_FOLDER.glob('*pdf'))) == 0: #if we have pdfs uploaded, we have to ask for files
            st.error('Add files .pdf to start chatting')
        else:
            st.success('Starting chat...')
            retriever = create_retriever()
            chain, memory = create_chain_and_memory(retriever)

            st.session_state['chain'] = chain
            st.session_state['memory'] = memory

            st.rerun()
            
def app_answer(question: str) -> str | None:
    normalized = question.lower().strip()

    if normalized in {"what can you do?", "what can you answer?"}:
        return "I can answer questions about the PDFs you uploaded."

    if normalized in {
        "what documents do you have?",
        "what do you have uploaded?",
        "which files do i have?",
    }:
        files = [file.name for file in FILES_FOLDER.glob("*.pdf")]
        return "You uploaded:\n" + "\n".join(f"- {file}" for file in files)

    return None

def chat_window():
    st.markdown(
    "<h2 style='text-align: center;'>🤖 Welcome to Chat PDF</h2>",
    unsafe_allow_html=True
    )
    
    if not 'chain' in st.session_state:
        st.error('Add files .pdf to start chatting')
        st.stop()
     
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

        answer = app_answer(input)

        if answer is None:
            answer = chain.invoke(input)
        
        memory.add_ai_message(answer)
        st.rerun()
    

def main():
    with st.sidebar:
        sidebar()
    
    chat_window()
        

if __name__ == "__main__":
    main()

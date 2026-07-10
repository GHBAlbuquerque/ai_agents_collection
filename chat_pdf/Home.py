import streamlit as st
from pathlib import Path
import time 

FILES_FOLDER = Path(__file__).parent / 'files'

def chat_bot_chain():
    st.session_state['chain'] = True
    time.sleep(1)
    pass

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
    
    if st.button(label_button, use_container_width=True):
        if len(list(FILES_FOLDER.glob('*pdf'))) == 0: #if we have pdfs uploaded, we have to ask for files
            st.error('Add files .pdf to start chatting')
        else:
            st.success('Starting chat...')
            chat_bot_chain()
            st.rerun()


def main():
    with st.sidebar:
        sidebar()
    pass
        

if __name__ == "__main__":
    main()

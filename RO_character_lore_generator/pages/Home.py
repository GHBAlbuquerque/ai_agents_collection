import streamlit as st

from properties import ALIGNMENT_OPTIONS, CLASSES_OPTIONS, GENDER_OPTIONS, LOCATIONS_OPTIONS
from ingestion import create_retriever
from agent import config_lore_chain

def init():
    if 'setup_complete' not in st.session_state:
        st.session_state['setup_complete'] = False    
    
    if 'chain' not in st.session_state or 'memory' not in st.session_state:
        with st.spinner("Initializing Vector Database..."):
            retriever = create_retriever()
            chain = config_lore_chain(retriever)
            
            st.session_state['chain'] = chain

def setup_page():
    st.markdown("<h2 style='text-align: center;'>📝 Character Setup</h2>", unsafe_allow_html=True) 
    
    with st.form("character_setup_form"):
        st.write("Please provide the details to generate your RO character:")
        
        char_name = st.text_input("Character Name (Optional)", max_chars=200)
        char_class = st.selectbox(label="Character Class (Required)*", options=CLASSES_OPTIONS)
        gender = st.selectbox("Gender (Required)*", GENDER_OPTIONS)
        birth_location = st.selectbox(label="Birth Location (Optional)", options=LOCATIONS_OPTIONS)
        char_age_input = st.text_input("Character Age (Optional)")
        char_alignment = st.selectbox(label="Character Alignment (Optional)*", options=ALIGNMENT_OPTIONS)
        description = st.text_area("Brief Description (Optional)*")
        
        submitted = st.form_submit_button("Generate Character Lore", type="primary")
        
        if submitted:
            if not char_class or not gender:
                st.error("⚠️ Please fill in all required fields (Class and Gender).") 
            else:
                char_age = int(char_age_input) if char_age_input.strip().isdigit() else None
                
                st.session_state['char_params'] = {
                    "character_name": char_name,
                    "character_class": char_class,
                    "gender": gender,
                    "birth_location": birth_location,
                    "character_age": char_age,
                    "char_alignment": char_alignment,
                    "description": description
                }
                st.session_state['setup_complete'] = True
                st.rerun()
                
def character_lore_page():
    st.write("Welcome to your Character Lore page!")

def main():
    init()
    
    if not st.session_state['setup_complete']:
        setup_page()
    else:
        character_lore_page()
    
if __name__ == "__main__":
    main()


# def chat_window():
    
#     st.markdown(
#     "<h2 style='text-align: center;'> Welcome to RO Character Lore Generator</h2>",
#     unsafe_allow_html=True
#     )
     
#     chain = st.session_state['chain']
#     memory = st.session_state['memory']
#     history = memory.messages
    
#     container = st.container()
#     for message in history:
#         chat = container.chat_message(message.type)
#         chat.markdown(message.content)
        
#     input = st.chat_input("Ask me anything!")
#     if input:
#         memory.add_user_message(input)
        
#         chat = container.chat_message('human')
#         chat.markdown(input)
        
#         chat = container.chat_message('ai')
#         chat.markdown("Generating answer...")

#         answer = chain.invoke(input)
#         formatted_answer = answer.replace('\n', '\n\n')
        
#         memory.add_ai_message(formatted_answer)
#         st.rerun()
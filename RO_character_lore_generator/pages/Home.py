import streamlit as st

from properties import ALIGNMENT_OPTIONS, CLASSES_OPTIONS, GENDER_OPTIONS, LOCATIONS_OPTIONS
from ingestion import create_retriever
from agent import config_lore_chain
from parser import parse_lore_output

def init():
    if 'setup_complete' not in st.session_state:
        st.session_state['setup_complete'] = False    
    
    if 'chain' not in st.session_state or 'memory' not in st.session_state:
        with st.spinner("Initializing Vector Database..."):
            retriever = create_retriever()
            chain = config_lore_chain(retriever)
            
            st.session_state['chain'] = chain

def setup_page():
    st.markdown("<h2 style='text-align: center;'> RO Character Lore Generator</h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>📝 Character Setup</h3>", unsafe_allow_html=True)
    
    st.write("Please provide the details to generate your RO character:")
            
    character_name = st.text_input("Character Name (Optional)", max_chars=200)
    character_class = st.selectbox(label="Character Class (Required)*", options=CLASSES_OPTIONS)
    gender = st.selectbox("Gender (Required)*", GENDER_OPTIONS)
    birth_location = st.selectbox(label="Birth Location (Optional)", options=LOCATIONS_OPTIONS)
    char_age_input = st.text_input("Character Age (Optional)")
    character_alignment = st.selectbox(label="Character Alignment (Optional)*", options=ALIGNMENT_OPTIONS)
    description = st.text_area("Brief Description (Optional)*")
    
    #TODO disable button
    if st.button("Generate Character Lore", type="primary", use_container_width=True,):
        if not character_class or not gender:
            st.error("⚠️ Please fill in all required fields (Class and Gender).") 
        else:
            character_age = int(char_age_input) if char_age_input.strip().isdigit() else None
            
            character_params = {
                "character_name": character_name,
                "character_class": character_class,
                "gender": gender,
                "birth_location": birth_location,
                "character_age": character_age,
                "character_alignment": character_alignment,
                "description": description
            }
                
            st.session_state['character_params'] = character_params
            chain = st.session_state['chain']
            
            with st.spinner("Generating your character lore..."):
                result = chain.invoke(character_params)
                st.session_state['generated_lore'] = result
            
            st.session_state['setup_complete'] = True
            st.rerun()
                
def character_lore_page():
    st.markdown("<h2 style='text-align: center;'> RO Character Lore Generator</h2>", unsafe_allow_html=True)
    
    generated_lore= st.session_state['generated_lore']
    
    if generated_lore:
        data = parse_lore_output(generated_lore)
        
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Name", data.get("name", "Unknown"))
                st.metric("Class", data.get("class", ""))
            with col2:
                st.metric("Gender", data.get("gender", ""))
                st.metric("Birthplace", data.get("place_of_birth", ""))
                
            st.subheader("Role")
            st.write(data.get("role", ""))
            
            st.subheader("Detailed Description")
            st.write(data.get("description", ""))
            
            st.subheader("📖 Read Full Character Acts")
            with st.container(border=True):
                st.markdown(f"**Act I:** {data.get('act_1')}")
                st.markdown(f"**Act II:** {data.get('act_2')}")
                st.markdown(f"**Act III:** {data.get('act_3')}")
                st.markdown(f"**Act IV:** {data.get('act_4')}")
                
            st.code(data.get("metadata", ""))
        
    if st.button("Go back to character creation", type="secondary", use_container_width=True):
        st.session_state['setup_complete'] = False
        st.rerun()

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
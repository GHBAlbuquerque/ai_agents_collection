import streamlit as st

from properties import ALIGNMENT_OPTIONS, CLASSES_OPTIONS, GENDER_OPTIONS, LOCATIONS_OPTIONS
from ingestion import create_retriever
from agent import config_lore_chain
from parser import parse_lore_output
from output_file_generator import save_txt_to_system, create_pdf_from_string

def init():
    if 'setup_complete' not in st.session_state:
        st.session_state['setup_complete'] = False
    
    if "is_generating_lore" not in st.session_state:
        st.session_state["is_generating_lore"] = False
        
    if "is_generating_pdf" not in st.session_state:
        st.session_state["is_generating_pdf"] = False
        
    if "pdf_data" not in st.session_state:
        st.session_state["pdf_data"] = False
    
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
    
    generate_button = st.button("Generate Character Lore", type="primary", use_container_width=True, disabled=st.session_state['is_generating_lore'])
    
    if generate_button:
        if not character_class or not gender:
            st.error("⚠️ Please fill in all required fields (Class and Gender).") 
        else:
            st.session_state['is_generating_lore'] = True
            st.rerun()
            
    if st.session_state['is_generating_lore'] and not st.session_state['setup_complete']:
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
    
    generated_lore = st.session_state['generated_lore']
    
    if generated_lore:
        data = parse_lore_output(generated_lore)
        file_name = f"{data.get('name', 'Character')}_Lore"
        save_txt_to_system(generated_lore, file_name)
        
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
    
        pdf_button = st.button(label="Geneate PDF", 
                            type="primary", 
                            disabled=st.session_state['is_generating_pdf'], 
                            use_container_width=True)
        
        if pdf_button:
            st.session_state['is_generating_pdf'] = True
            st.session_state["pdf_data"] = None
            st.rerun()
        
        if st.session_state['is_generating_pdf'] and not st.session_state["pdf_data"]:
            with st.spinner("Generating your character lore PDF..."):
                pdf_bytes = create_pdf_from_string(generated_lore)
                st.session_state["pdf_data"] = pdf_bytes
                st.session_state['is_generating_pdf'] = False
        
        if st.session_state['pdf_data']:
            
            st.download_button(
                label="Download Lore PDF",
                data= st.session_state["pdf_data"],
                file_name=file_name+".pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
    
    if st.button("Go back to character creation", type="secondary", use_container_width=True):
        reset_session_state()
        st.rerun()


def reset_session_state():
    st.session_state['setup_complete'] = False
    st.session_state["is_generating_lore"] = False
    st.session_state["is_generating_pdf"] = False
    st.session_state["pdf_data"] = None
    st.session_state["character_params"] = None

def inspect_session_state():
    with st.expander("🔍 Inspect Session State"):
        st.write(st.session_state)

def main():
    init()
    
    if not st.session_state['setup_complete']:
        setup_page()
    else:
        character_lore_page()
    
if __name__ == "__main__":
    main()
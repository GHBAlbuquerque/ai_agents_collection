import streamlit as st

home = st.Page("pages/Home.py", title="Home", default=True)

pg = st.navigation([home])

pg.run()
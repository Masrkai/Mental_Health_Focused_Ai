import time
import streamlit as st

# Function to print animated text in Streamlit
def print_animated_txt(text):
    placeholder = st.empty()  
    for char in text:
        placeholder.markdown(char, unsafe_allow_html=True)  
        time.sleep(0.05)  
    placeholder.markdown(text, unsafe_allow_html=True) 
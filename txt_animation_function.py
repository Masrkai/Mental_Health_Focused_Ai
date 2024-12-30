import time  # For introducing delays
import streamlit as st  # Streamlit for building interactive web applications

# Function to print animated text in Streamlit
def print_animated_txt(text):
    """
    Displays an animated text effect in a Streamlit app, showing one character at a time.

    Parameters:
    text (str): The text to display in an animated fashion.
    """
    placeholder = st.empty()  # Create a placeholder for dynamic content updates
    for char in text:  # Iterate through each character in the provided text
        placeholder.markdown(char, unsafe_allow_html=True)  # Display the character in the placeholder
        time.sleep(0.05)  # Pause briefly before displaying the next character
    placeholder.markdown(text, unsafe_allow_html=True)  # Display the full text after the animation

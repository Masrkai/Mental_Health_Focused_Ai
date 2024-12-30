import streamlit as st  # For interactive web applications
from streamlit_option_menu import option_menu  # For creating a customizable option menu
from Language_Model import ChatBot  # Importing the custom ChatBot class
from Speech_to_text import main_stt  # Importing the main function for speech-to-text conversion
import asyncio  # For asynchronous processing
import time  # For delays

# Initialize ChatBot instance
chatbot = ChatBot()  # Creates an instance of the ChatBot class for use in the app

# Apply custom CSS for styling the Streamlit app
st.markdown("""
<style>
    /* Custom color variables for theming */
    :root {
        --primary-color: #A6B37D;
        --background-color: #FEFAE0;
        --secondary-bg-color: #B99470;
        --text-color: #C0C78C;
    }
    /* Style definitions for various app elements */
    .main { ... }  /* Main app container styling */
    .stApp { ... }  /* Streamlit's background styling */
    .css-1d391kg { ... }  /* Sidebar styling */
    /* Additional animations, buttons, and text area styling */
</style>
<script>
    // JavaScript for handling sidebar animations
    const toggleSidebar = () => {
        const sidebar = document.querySelector('.css-1d391kg');
        sidebar.classList.toggle('sidebar-hidden');
        sidebar.classList.toggle('sidebar-visible');
    }
</script>
""", unsafe_allow_html=True)  # Includes CSS and JS for advanced customization

# Mock user database
USER_DB = {
    "admin": "admin123",
    "user1": "password1",
    "user2": "password2"
}

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "recording" not in st.session_state:
    st.session_state.recording = False
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False
if "sign_up_success" not in st.session_state:
    st.session_state.sign_up_success = False

def signin_signup():
    """
    Handles user sign-in and sign-up functionality using a Streamlit option menu.
    """
    selected = option_menu(
        menu_title=None,  # No title for the menu
        options=["Sign In", "Sign Up"],  # Options for the menu
        icons=["person", "person-add"],  # Icons for the options
        menu_icon="cast",  # Icon for the menu
        default_index=0,  # Default selected option
        orientation="horizontal",  # Horizontal menu orientation
        styles={...}  # Styling for the menu
    )
    
    if selected == "Sign In":  # If "Sign In" is selected
        st.title("Sign In")  # Display sign-in title
        with st.form("signin_form", clear_on_submit=True):  # Sign-in form
            username = st.text_input("Username")  # Username input
            password = st.text_input("Password", type="password")  # Password input
            submitted = st.form_submit_button("Sign In")  # Submit button
            
            if submitted:  # If the form is submitted
                if USER_DB.get(username) == password:  # Validate credentials
                    st.success(f"Welcome, {username}!")  # Welcome message
                    st.session_state.authenticated = True  # Set authentication state
                    st.session_state.username = username  # Save username
                    st.rerun()  # Reload the app
                else:
                    st.error("Invalid credentials.")  # Error message

    elif selected == "Sign Up":  # If "Sign Up" is selected
        st.title("Sign Up")  # Display sign-up title
        with st.form("signup_form", clear_on_submit=True):  # Sign-up form
            username = st.text_input("Username")  # Username input
            password = st.text_input("Password", type="password")  # Password input
            confirm_password = st.text_input("Confirm Password", type="password")  # Password confirmation
            submitted = st.form_submit_button("Sign Up")  # Submit button
            
            if submitted:  # If the form is submitted
                if username in USER_DB:  # Check if the username already exists
                    st.error("Username already exists.")  # Error message
                elif password != confirm_password:  # Check if passwords match
                    st.error("Passwords do not match.")  # Error message
                elif not username or not password:  # Check for empty fields
                    st.error("Please fill in all fields.")  # Error message
                else:
                    USER_DB[username] = password  # Add the new user to the database
                    st.success("Account created successfully! Please sign in.")  # Success message
                    st.session_state.sign_up_success = True  # Update session state
                    time.sleep(1)  # Delay for UX
                    st.rerun()  # Reload the app

def sidebar():
    """
    Displays the sidebar with menu options for signed-in users.
    """
    with st.sidebar:
        st.title("Menu")  # Sidebar title
        if st.button("Sign Out"):  # Sign-out button
            st.session_state.authenticated = False  # Reset authentication state
            st.session_state.username = None  # Clear username
            st.rerun()  # Reload the app

        new_personality = st.text_input("Update AI Personality:")  # Input for new AI personality
        if st.button("Update Personality"):  # Update personality button
            chatbot.update_personality(new_personality)  # Update personality in ChatBot
            st.success("Personality updated!")  # Success message

def main_ui():
    """
    Displays the main user interface with options for voice input and AI interaction.
    """
    if st.session_state.show_sidebar:
        sidebar()  # Show sidebar if toggled on

    st.title("AI Assistant Dashboard")  # App title
    st.markdown(f"Welcome back, **{st.session_state.username}**! 👋")  # Welcome message
    
    col1, col2 = st.columns([2, 1])  # Create two columns for content
    
    with col1:
        if st.button("🎤 Start/Stop Recording"):  # Toggle recording button
            st.session_state.recording = not st.session_state.recording

        if st.session_state.recording:  # If recording is active
            try:
                while True:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    recorded_text = loop.run_until_complete(main_stt())  # Perform STT
                    
                    if recorded_text.strip():  # If STT yields results
                        ai_response = chatbot.get_response(recorded_text)  # Get AI response
                        st.text_area("🤖 AI Response", value=ai_response, height=200)  # Display AI response
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")  # Handle errors
        else:
            st.info("🎤 Click 'Start Recording' to begin")  # Recording instructions

if __name__ == "__main__":
    if not st.session_state.authenticated:  # If not authenticated, show login/signup
        signin_signup()
    else:
        main_ui()  # Show the main UI for authenticated users

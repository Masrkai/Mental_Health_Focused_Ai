# Import necessary libraries
import streamlit as st  # Web framework for creating interactive web apps
from streamlit_option_menu import option_menu  # For creating styled navigation menus
from Language_Model import ChatBot  # Import custom ChatBot class for AI interactions
from Speech_to_text import main_stt  # Import speech-to-text module
import asyncio  # For asynchronous programming
import time  # To add delays in execution

# Initialize ChatBot instance for AI functionality
chatbot = ChatBot()

# Custom CSS for Streamlit styling with new color palette and animations
st.markdown("""
<style>
    /* Custom color variables */
    :root {
        --primary-color: #A6B37D;
        --background-color: #FEFAE0;
        --secondary-bg-color: #B99470;
        --text-color: #C0C78C;
    }

    /* Styling the main container */
    .main {
        padding: 2rem;
        background-color: var(--background-color);
        font-family: 'sans serif';
    }
    
    /* Set background color for the app by Override Streamlit's default background */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Sidebar styling with animation states */
    .css-1d391kg {
        padding-top: 3.5rem;
        background-color: var(--secondary-bg-color);
        transition: transform 0.3s ease-in-out;
    }
    
    /* Toggle for sidebar visibility */
    .sidebar-hidden {
        transform: translateX(-100%);
    }
    
    .sidebar-visible {
        transform: translateX(0);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom toggle button for the sidebar */
    .sidebar-toggle {
        position: fixed;
        left: 0;
        top: 0;
        padding: 12px 15px;
        background: var(--primary-color);
        border: none;
        color: white;
        z-index: 999;
        border-radius: 0 0 5px 0;
        transition: all 0.3s ease;
    }
    
    .sidebar-toggle:hover {
        background: var(--secondary-bg-color);
        padding-right: 25px;
    }

    /* Styling for Card-like containers */
    .stForm {
        background-color: var(--secondary-bg-color);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .stForm:hover {
        transform: translateY(-5px);
    }
    
    /* Styling buttons */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary-bg-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Text area styling */
    .stTextArea>div>div>textarea {
        background-color: white;
        color: var(--text-color);
        border: 1px solid var(--primary-color);
        border-radius: 5px;
        transition: border 0.3s ease;
    }
    
    .stTextArea>div>div>textarea:focus {
        border: 2px solid var(--primary-color);
        box-shadow: 0 0 5px rgba(166, 179, 125, 0.3);
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: var(--primary-color);
        margin-bottom: 1.5rem;
        font-family: 'sans serif';
    }
    
    /* Info messages styling */
    .stAlert {
        background-color: var(--secondary-bg-color);
        border-radius: 5px;
        color: white;
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Text input styling */
    .stTextInput>div>div>input {
        background-color: white;
        color: var(--text-color);
        border: 1px solid var(--primary-color);
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border: 2px solid var(--primary-color);
        box-shadow: 0 0 5px rgba(166, 179, 125, 0.3);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    /* Animation classes */
    .animate-fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    .animate-slide-in {
        animation: slideIn 0.3s ease-in-out;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-color);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-bg-color);
    }
</style>

<script>
    // JavaScript for handling sidebar animations
    const toggleSidebar = () => {
        const sidebar = document.querySelector('.css-1d391kg');
        sidebar.classList.toggle('sidebar-hidden');
        sidebar.classList.toggle('sidebar-visible');
    }
</script>
""", unsafe_allow_html=True)  # Injects the CSS into the app

# Rest of your Python code remains the same as in the previous artifact, starting from:
# Mock user database
USER_DB = {
    "admin": "admin123",
    "user1": "password1",
    "user2": "password2"
}

# Initialize session states if not already present
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False  # Tracks user authentication status
if "username" not in st.session_state:
    st.session_state.username = None  # Stores the logged-in username
if "recording" not in st.session_state:
    st.session_state.recording = False  # Tracks recording status
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False  # Tracks sidebar visibility
if "sign_up_success" not in st.session_state:
    st.session_state.sign_up_success = False  # Tracks sign-up success

# Function for handling Sign In and Sign Up
def signin_signup():
    # Display Sign In / Sign Up options as a horizontal menu
    selected = option_menu(
        menu_title=None,
        options=["Sign In", "Sign Up"],  # Two options
        icons=["person", "person-add"],  # Icons for the options
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={  # Custom styles for the menu
            "container": {"padding": "0!important", "background-color": "#B99470"},
            "icon": {"color": "#A6B37D", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#A6B37D",
                "color": "#FEFAE0"
            },
            "nav-link-selected": {"background-color": "#A6B37D"},
        }
    )
    
    # Sign In functionality
    if selected == "Sign In":
        st.title("Sign In")  # Page title
        with st.form("signin_form", clear_on_submit=True):  # Create a sign-in form
            col1, col2 = st.columns([3, 1])  # Layout with two columns
            with col1:
                username = st.text_input("Username")  # Username input
                password = st.text_input("Password", type="password")  # Password input
            with col2:
                st.write("")  # Placeholder for alignment
                submitted = st.form_submit_button("Sign In")  # Submit button
            
            if submitted:  # If the form is submitted
                if USER_DB.get(username) == password:  # Validate credentials
                    st.success(f"Welcome, {username}!")  # Success message
                    st.session_state.authenticated = True  # Mark as authenticated
                    st.session_state.username = username  # Save username
                    st.rerun()  # Reload the app
                else:
                    st.error("Invalid credentials.")  # Show error for invalid login

    # Sign Up functionality
    elif selected == "Sign Up":
        st.title("Sign Up")  # Page title
        with st.form("signup_form", clear_on_submit=True):  # Create a sign-up form
            username = st.text_input("Username")  # Username input
            col1, col2 = st.columns(2)  # Layout with two columns
            with col1:
                password = st.text_input("Password", type="password")  # Password input
            with col2:
                confirm_password = st.text_input("Confirm Password", type="password")  # Confirm password input
            submitted = st.form_submit_button("Sign Up")  # Submit button
            
            if submitted:  # If the form is submitted
                if username in USER_DB:  # Check if username exists
                    st.error("Username already exists.")  # Show error
                elif password != confirm_password:  # Check for matching passwords
                    st.error("Passwords do not match.")  # Show error
                elif not username or not password:  # Check for empty fields
                    st.error("Please fill in all fields.")  # Show error
                else:
                    USER_DB[username] = password  # Save new user
                    st.success("Account created successfully! Please sign in.")  # Success message
                    st.session_state.sign_up_success = True  # Update session state
                    st.session_state.authenticated = True  # Mark as authenticated
                    st.session_state.username = username  # Save username
                    time.sleep(1)  # Short delay before redirect
                    st.rerun()  # Reload the app

# Sidebar functionality
def sidebar():
    with st.sidebar:  # Define sidebar content
        st.title("Menu")  # Sidebar title
        st.markdown("---")  # Divider
        if st.button("Sign Out", key="signout"):  # Sign out button
            st.session_state.authenticated = False  # Reset authentication
            st.session_state.username = None  # Clear username
            st.rerun()  # Reload the app
        
        st.markdown("---")  # Divider
        st.markdown("### Settings")  # Settings section
        if st.button("Clear History"):  # Button to clear conversation history
            chatbot.history.clear_history()  # Clear chatbot history
            st.success("Conversation history cleared!")  # Success message
        
        # Input to update AI personality
        new_personality = st.text_input("Update AI Personality:")
        if st.button("Update Personality"):  # Button to update personality
            if new_personality.strip():
                chatbot.update_personality(new_personality)  # Update chatbot personality
                st.success("Personality updated!")  # Success message

# Main user interface
def main_ui():
    if st.button("☰", key="toggle_sidebar"):  # Sidebar toggle button
        st.session_state.show_sidebar = not st.session_state.show_sidebar  # Toggle sidebar visibility

    if st.session_state.show_sidebar:  # If sidebar is visible
        sidebar()  # Display sidebar

    st.title("AI Assistant Dashboard")  # Main title
    st.markdown(f"Welcome back, **{st.session_state.username}**! 👋")  # Welcome message
    
    col1, col2 = st.columns([2, 1])  # Two columns for layout
    
    # Voice interface
    with col1:
        st.subheader("Voice Interface")  # Section header
        if st.button("🎤 Start/Stop Recording", key="record_button"):  # Start/Stop recording button
            st.session_state.recording = not st.session_state.recording  # Toggle recording state

        if st.session_state.recording:  # If recording
            st.info("🎙️ Recording in progress...")  # Recording message
            try:
                while True:  # Continuously record speech
                    loop = asyncio.new_event_loop()  # Create new event loop
                    asyncio.set_event_loop(loop)  # Set event loop
                    recorded_text = loop.run_until_complete(main_stt())  # Get recorded text
                    
                    if recorded_text.strip():  # If speech is detected
                        st.text_area("📝 Speech-to-Text Output", value=recorded_text, height=100)  # Display speech output
                        if recorded_text.lower() == "exit.":  # Stop recording if "exit." is said
                            st.session_state.recording = False
                            break
                        
                        with st.spinner("🤖 Generating response..."):  # Show spinner while processing
                            ai_response = chatbot.get_response(recorded_text)  # Get AI response
                        
                        st.text_area("🤖 AI Response", value=ai_response, height=200)  # Display AI response
                        st.session_state.recording = True  # Continue recording
                    else:
                        st.warning("🔇 No speech detected. Please try again.")  # Warning for no speech
            except Exception as e:  # Handle exceptions
                st.error(f"❌ Error: {str(e)}")  # Display error
                st.session_state.recording = False
        else:
            st.info("🎤 Click 'Start Recording' to begin")  # Instructions for starting recording
    
    # Quick actions
    with col2:
        st.subheader("Quick Actions")  # Section header
        st.markdown("""
        Voice Commands:
        - Say "exit." to stop recording
        - Say "clear." to clear history
        - Say "personality." to update AI personality
        """)

# Run the app
if __name__ == "__main__":
    if not st.session_state.authenticated:  # If user is not authenticated
        signin_signup()  # Show Sign In/Sign Up
    else:
        main_ui()  # Show main UI

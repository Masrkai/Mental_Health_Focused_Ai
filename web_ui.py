import streamlit as st
from streamlit_option_menu import option_menu
from Language_Model import ChatBot
from Speech_to_text import main_stt
import asyncio
import time

# Initialize ChatBot instance
chatbot = ChatBot()

# Custom CSS for styling with new color palette and animations
st.markdown("""
<style>
    /* Theme colors */
    :root {
        --primary-color: #A6B37D;
        --background-color: #FEFAE0;
        --secondary-bg-color: #B99470;
        --text-color: #C0C78C;
    }

    /* Main container styling */
    .main {
        padding: 2rem;
        background-color: var(--background-color);
        font-family: 'sans serif';
    }
    
    /* Override Streamlit's default background */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Sidebar styling with animation */
    .css-1d391kg {
        padding-top: 3.5rem;
        background-color: var(--secondary-bg-color);
        transition: transform 0.3s ease-in-out;
    }
    
    /* Sidebar animation states */
    .sidebar-hidden {
        transform: translateX(-100%);
    }
    
    .sidebar-visible {
        transform: translateX(0);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom sidebar toggle button */
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
    
    /* Card-like containers with new colors */
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
    
    /* Custom button styling */
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
""", unsafe_allow_html=True)

# Rest of your Python code remains the same as in the previous artifact, starting from:
# Mock user database
USER_DB = {
    "admin": "admin123",
    "user1": "password1",
    "user2": "password2"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "recording" not in st.session_state:
    st.session_state.recording = False
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False
if "sign_up_success" not in st.session_state:  # Add this line
    st.session_state.sign_up_success = False

def signin_signup():
    selected = option_menu(
        menu_title=None,
        options=["Sign In", "Sign Up"],
        icons=["person", "person-add"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
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
    
    if selected == "Sign In":
        st.title("Sign In")
        with st.form("signin_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
            with col2:
                st.write("")
                st.write("")
                submitted = st.form_submit_button("Sign In")
            
            if submitted:
                if USER_DB.get(username) == password:
                    st.success(f"Welcome, {username}!")
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

    elif selected == "Sign Up":
        st.title("Sign Up")
        with st.form("signup_form", clear_on_submit=True):
            username = st.text_input("Username")
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input("Password", type="password")
            with col2:
                confirm_password = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Sign Up")
            
            if submitted:
                if username in USER_DB:
                    st.error("Username already exists.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    USER_DB[username] = password
                    st.success("Account created successfully! Please sign in.")
                    st.session_state.sign_up_success = True
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    time.sleep(1)  # Short delay before redirect
                    st.rerun() 

def sidebar():
    with st.sidebar:
        st.title("Menu")
        st.markdown("---")
        if st.button("Sign Out", key="signout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Settings")
        if st.button("Clear History"):
            chatbot.history.clear_history()
            st.success("Conversation history cleared!")
        
        new_personality = st.text_input("Update AI Personality:")
        if st.button("Update Personality"):
            if new_personality.strip():
                chatbot.update_personality(new_personality)
                st.success("Personality updated!")

def main_ui():
    # Toggle sidebar button
    if st.button("☰", key="toggle_sidebar"):
        st.session_state.show_sidebar = not st.session_state.show_sidebar

    if st.session_state.show_sidebar:
        sidebar()

    # Main content
    st.title("AI Assistant Dashboard")
    st.markdown(f"Welcome back, **{st.session_state.username}**! 👋")
    
    # Create two columns for the main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Voice Interface")
        if st.button("🎤 Start/Stop Recording", key="record_button"):
            st.session_state.recording = not st.session_state.recording

        if st.session_state.recording:
            st.info("🎙️ Recording in progress...")
            try:
                while True:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    recorded_text = loop.run_until_complete(main_stt())
                    
                    if recorded_text.strip():
                        st.text_area("📝 Speech-to-Text Output", value=recorded_text, height=100)
                        if recorded_text.lower() == "exit.":
                            st.session_state.recording = False
                            break
                        
                        # Get AI response
                        with st.spinner("🤖 Generating response..."):
                            ai_response = chatbot.get_response(recorded_text)
                        
                        # Display AI response
                        st.text_area("🤖 AI Response", value=ai_response, height=200)
                        
                        # Automatically continue recording
                        st.session_state.recording = True
                    else:
                        st.warning("🔇 No speech detected. Please try again.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.recording = False
        else:
            st.info("🎤 Click 'Start Recording' to begin")
    
    with col2:
        st.subheader("Quick Actions")
        st.markdown("""
        Voice Commands:
        - Say "exit." to stop recording
        - Say "clear." to clear history
        - Say "personality." to update AI personality
        """)

# Run the App
if __name__ == "__main__":
    if not st.session_state.authenticated:
        signin_signup()
    else:
        main_ui()

# Importing required libraries and modules
import os  # Provides functionalities for interacting with the operating system
import json  # For handling JSON data
import datetime  # For working with dates and times
import argparse  # To parse command-line arguments
import readline  # Improves terminal input handling by enabling line editing and history
from dotenv import load_dotenv  # Loads environment variables from a .env file
from typing import List, Dict, Union  # For type hinting complex data structures
from dataclasses import dataclass, asdict  # Simplifies class creation and serialization
from huggingface_hub import InferenceClient  # Used to interact with Hugging Face's inference API
from Speech_to_text import main_stt  # Placeholder for a custom speech-to-text function/module
import asyncio  # Supports asynchronous programming
from txt_animation_function import print_animated_txt  # Placeholder for a custom text animation function

# Define a data class for individual messages
@dataclass
class Message:
    role: str  # Specifies the role of the message sender (e.g., user or assistant)
    content: Union[str, List[Dict]]  # Message content, can be plain text or structured
    timestamp: str  # Timestamp of when the message was created

# Manages the conversation history, including saving/loading messages
class ConversationHistory:
    def __init__(self, history_file: str = "conversation_history.json"):
        self.history_file = history_file  # Path to the file storing conversation history
        self.messages: List[Message] = []  # List to store Message objects
        self.load_history()  # Load history from the file on initialization

    def add_message(self, role: str, content: Union[str, List[Dict]]):
        # Adds a new message to the history
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
        message = Message(role=role, content=content, timestamp=timestamp)  # Create a new message
        self.messages.append(message)  # Add the message to the list
        self.save_history()  # Save the updated history to the file

    def load_history(self):
        # Loads the conversation history from the file
        if os.path.exists(self.history_file):  # Check if the file exists
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)  # Load the JSON data
                    self.messages = [Message(**msg) for msg in data]  # Deserialize messages
            except json.JSONDecodeError:
                print("Warning: Could not load history file. Starting fresh.")  # Handle file corruption

    def save_history(self):
        # Saves the conversation history to the file
        with open(self.history_file, 'w') as f:
            json.dump([asdict(msg) for msg in self.messages], f, indent=2)  # Serialize messages as JSON

    def clear_history(self):
        # Clears the conversation history
        self.messages = []  # Empty the list of messages
        if os.path.exists(self.history_file):  # Delete the history file if it exists
            os.remove(self.history_file)

# Represents the chatbot and its operations
class ChatBot:
    def __init__(self, model_name: str = "meta-llama/Llama-3.2-11B-Vision-Instruct"):
        load_dotenv()  # Load environment variables from .env file
        self.token = os.getenv("HF_API_KEY")  # Get the API key from environment variables
        if not self.token:
            raise ValueError("API key not found. Please set HF_API_KEY in your .env file.")  # Error if key missing

        self.model_name = model_name  # Name of the model to be used
        self.client = InferenceClient(api_key=self.token)  # Initialize Hugging Face inference client
        self.history = ConversationHistory()  # Initialize conversation history manager
        self.personality = self.load_personality("personality.txt")  # Load chatbot personality from file

    def load_personality(self, file_path: str) -> str:
        # Loads the chatbot's personality from a file
        if os.path.exists(file_path):  # Check if the personality file exists
            with open(file_path, 'r') as f:
                return f.read().strip()  # Read and return the personality text
        return "You are a helpful assistant. Answer questions clearly and concisely."  # Default personality

    def update_personality(self, new_personality: str):
        # Updates the chatbot's personality and saves it to a file
        with open("personality.txt", 'w') as f:
            f.write(new_personality)  # Save the new personality text to file
        self.personality = new_personality  # Update the in-memory personality

    def format_conversation(self) -> List[Dict]:
        # Formats the conversation history for sending to the inference API
        formatted_messages = []

        # Add system message with the chatbot's personality
        formatted_messages.append({
            "role": "system",
            "content": [{"type": "text", "text": self.personality}]
        })

        # Add the last 10 messages from the history
        for msg in self.history.messages[-10:]:
            # Ensure content is structured as expected
            if isinstance(msg.content, str):
                formatted_content = [{"type": "text", "text": msg.content}]
            else:
                formatted_content = msg.content

            formatted_messages.append({
                "role": msg.role,
                "content": formatted_content
            })

        return formatted_messages

    def get_response(self, user_input: str) -> str:
        # Gets a response from the chatbot model based on user input
        user_content = [{"type": "text", "text": user_input}]  # Format user input

        # Add user input to the conversation history
        self.history.add_message("user", user_content)

        try:
            # Prepare the conversation context
            messages = self.format_conversation()

            # Request a response from the model
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=500  # Limit the response length
            )

            # Extract the model's response
            model_response = completion.choices[0].message.content

            # Add model response to the history
            self.history.add_message("assistant", model_response)

            return model_response  # Return the response

        except Exception as e:
            # Handle errors and return error message
            error_msg = f"Error: {str(e)}"
            print(f"Debug info - Error occurred: {error_msg}")  # Log error details
            return error_msg

# Entry point for the chatbot application
async def main(user_input):
    parser = argparse.ArgumentParser(description="Terminal Chat Application")  # Command-line argument parser
    parser.add_argument("--model", default="meta-llama/Llama-3.2-11B-Vision-Instruct", help="Model name to use")
    args = parser.parse_args()  # Parse command-line arguments

    chatbot = ChatBot(model_name=args.model)  # Initialize the chatbot with the specified model

    try:
        if user_input.lower() == 'exit.':  # Exit command
            print("Goodbye!")
            return False
        elif user_input.lower() == 'clear.':  # Clear history command
            chatbot.history.clear_history()
            print("Conversation history cleared!")
        elif user_input.lower() == 'personality.':  # Update personality command
            new_personality = input("Enter new personality: ").strip()
            chatbot.update_personality(new_personality)
            print("Personality updated!")

        response = chatbot.get_response(user_input)  # Get chatbot response
        return response  # Return the response to the user
    except Exception as e:
        # Handle errors and log the details
        print(f"\nAn error occurred: {str(e)}")

# Script execution starts here
if __name__ == "__main__":
    asyncio.run(main())  # Run the main function as an asynchronous coroutine

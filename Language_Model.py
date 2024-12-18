import os
import json
import datetime
import argparse
import readline  # For better terminal input handling
from dotenv import load_dotenv
from typing import List, Dict, Union
from dataclasses import dataclass, asdict
from huggingface_hub import InferenceClient
from Speech_to_text import main_stt
import asyncio

@dataclass
class Message:
    role: str
    content: Union[str, List[Dict]]  # Updated to handle both text and structured content
    timestamp: str

class ConversationHistory:
    def __init__(self, history_file: str = "conversation_history.json"):
        self.history_file = history_file
        self.messages: List[Message] = []
        self.load_history()

    def add_message(self, role: str, content: Union[str, List[Dict]]):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = Message(role=role, content=content, timestamp=timestamp)
        self.messages.append(message)
        self.save_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.messages = [Message(**msg) for msg in data]
            except json.JSONDecodeError:
                print("Warning: Could not load history file. Starting fresh.")

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump([asdict(msg) for msg in self.messages], f, indent=2)

    def clear_history(self):
        self.messages = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

class ChatBot:
    def __init__(self, model_name: str = "meta-llama/Llama-3.2-11B-Vision-Instruct"):
        load_dotenv()
        self.token = os.getenv("HF_API_KEY")
        if not self.token:
            raise ValueError("API key not found. Please set HF_API_KEY in your .env file.")

        self.model_name = model_name
        self.client = InferenceClient(api_key=self.token)
        self.history = ConversationHistory()
        self.personality = self.load_personality("personality.txt")

    def load_personality(self, file_path: str) -> str:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read().strip()
        return "You are a helpful assistant. Answer questions clearly and concisely."

    def update_personality(self, new_personality: str):
        with open("personality.txt", 'w') as f:
            f.write(new_personality)
        self.personality = new_personality

    def format_conversation(self) -> List[Dict]:
        formatted_messages = []

        # Add system message with personality
        formatted_messages.append({
            "role": "system",
            "content": [{"type": "text", "text": self.personality}]
        })

        # Add conversation history
        for msg in self.history.messages[-10:]:  # Keep last 10 messages for context window
            # Format the content as expected by the API
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
        # Format user input as expected by the API
        user_content = [{"type": "text", "text": user_input}]

        # Add user message to history
        self.history.add_message("user", user_content)

        try:
            # Prepare the conversation context
            messages = self.format_conversation()

            # Get model response using the chat completions API
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=500
            )

            # Extract the model's response
            model_response = completion.choices[0].message.content

            # Add model response to history
            self.history.add_message("assistant", model_response)

            return model_response

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"Debug info - Error occurred: {error_msg}")  # Added for debugging
            return error_msg

async def main():
    parser = argparse.ArgumentParser(description="Terminal Chat Application")
    parser.add_argument("--model", default="meta-llama/Llama-3.2-11B-Vision-Instruct", help="Model name to use")
    args = parser.parse_args()

    chatbot = ChatBot(model_name=args.model)

    print(f"Chat initialized with model: {args.model}")
    print("Type 'exit' to quit, 'clear' to clear history, 'personality' to update personality")
    print("Current personality:", chatbot.personality)
    print("\nStart chatting!")

    while True:
        try:
            user_input = await main_stt()

            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'clear':
                chatbot.history.clear_history()
                print("Conversation history cleared!")
                continue
            elif user_input.lower() == 'personality':
                new_personality = input("Enter new personality: ").strip()
                chatbot.update_personality(new_personality)
                print("Personality updated!")
                continue
            elif not user_input:
                continue

            response = chatbot.get_response(user_input)
            print("\nAssistant:", response)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
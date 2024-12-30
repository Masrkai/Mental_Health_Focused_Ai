# Importing necessary libraries and modules
from RealtimeSTT import AudioToTextRecorder  # Custom module for real-time speech-to-text recording
import speech_recognition as sr  # Speech recognition library for converting audio to text
import time  # Provides time-related functions
  # Manages bidirectional text rendering (e.g., Arabic)
import asyncio  # Supports asynchronous programming

# Comments for installing CUDA, cuDNN, and related PyTorch dependencies for GPU support:
# Ensure CUDA and cuDNN are installed for GPU acceleration with PyTorch.
# Installation commands for different CUDA versions are provided below.

# For CUDA 11.8:
# pip install torch==2.5.1+cu118 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.x:
# pip install torch==2.5.1+cu121 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# Ensure that cuDNN is installed for your version of CUDA.
# If a powerful CPU is available, line 52 can be modified to switch from GPU (CUDA) to CPU.

# Regular expression to match Arabic characters


 # Matches text against Arabic character regex

async def process_text(recorded_text, log):
    """
    Processes the recorded text to check if it's Arabic and reshapes it accordingly.
    Logs the processed text (reshaped or plain) into the log.
    """
    print(f"Recorder Output: {recorded_text}")  # Display non-Arabic text as-is
    log.append(recorded_text)  # Add plain text to the log

async def recorder_and_recognizer(log, recorder):
    """
    Handles audio recording and text recognition.
    Processes recorded audio text and appends it to the log.
    """
    try:
        recorded_text = recorder.text()  # Retrieve text from the audio recorder
        await process_text(recorded_text, log)  # Process the retrieved text
    except Exception as e:
        print(f"Error with AudioToTextRecorder: {e}")  # Handle recording errors gracefully
    return log  # Return the updated log

async def main_stt():
    """
    Main function to perform real-time speech-to-text recognition and text processing.
    Uses the AudioToTextRecorder to record and recognize speech.
    """
    log = []  # Initialize an empty log to store recognized text

    # Use the audio-to-text recorder with specified model and device settings
    with AudioToTextRecorder(model="tiny", device="cuda", compute_type="float32") as recorder:
        log = await recorder_and_recognizer(log, recorder)  # Perform recording and recognition
        await asyncio.sleep(0.005)  # Add a slight delay to simulate real-time processing

    return "\n".join(log)  # Join and return the log as a single string of text

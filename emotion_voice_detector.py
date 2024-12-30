import torch  # PyTorch library for deep learning and tensor computation
from speechbrain.inference import EncoderClassifier  # For pre-trained model inference using SpeechBrain

# Note:
# This script was originally designed to use the Whisper model for speech-to-text (STT).
# Audio files were saved as temporary .wav files in a folder before being processed.
# Subsequently, this script was modified to work without saving files.
# If a function for saving audio as a .wav file is required, let me know and I can provide it.

def detect_emotion(audio_path):
    """
    Detects emotions from an audio file using a pre-trained SpeechBrain model.

    Parameters:
    audio_path (str): Path to the audio file to process.

    Returns:
    dict: Contains detected emotion and corresponding probabilities.
          Returns None if an error occurs.
    """
    try:
        # Load the pre-trained emotion recognition model from SpeechBrain
        model = EncoderClassifier.from_hparams(
            source="speechbrain/emotion-recognition-wav2vec2",  # Pre-trained model source
            savedir="tmp_model"  # Directory to save the model locally
        )
        
        # Perform emotion classification on the given audio file
        prediction = model.classify_file(audio_path)  # Classify the emotions in the audio file
        emotion = prediction[0]  # Extract the predicted emotion label
        probabilities = prediction[3]  # Extract probabilities for each emotion
        
        # Return the emotion label and probabilities in a dictionary
        return {
            "emotion": emotion,
            "probabilities": probabilities
        }
    
    except Exception as e:
        # Handle and log errors gracefully
        print(f"Error in emotion detection: {e}")
        return None  # Return None if an error occurs

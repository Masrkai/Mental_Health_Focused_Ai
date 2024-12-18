import torch
from speechbrain.inference import EncoderClassifier
# note : i edited this script multiple of times when i was using whisper model
#        to get stt from audio file then save it as temp folder in wav format
#        then called this function in speech_to_text.py using the temp wav folder
#        then i modifed the stt code to make it that it doesnt save it as wav folder
#        if a function is needed to save wav file then ask me about it and i will provide it

def detect_emotion(audio_path):
    try:
        # Load the pre-trained model
        model = EncoderClassifier.from_hparams(
            source="speechbrain/emotion-recognition-wav2vec2",
            savedir="tmp_model"
        )
        
        # Perform emotion classification
        prediction = model.classify_file(audio_path)
        emotion = prediction[0]  
        probabilities = prediction[3]  
        
        return {
            "emotion": emotion,
            "probabilities": probabilities
        }
    
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return None

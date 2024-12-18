from RealtimeSTT import AudioToTextRecorder
import speech_recognition as sr
import time
import arabic_reshaper
import re
from bidi.algorithm import get_display
import asyncio

# install cuda and cuddenn for GPU support
# and based on that download torch and torchaudio
# for cuda 11.8 use torch 2.51 and torchaudio 2.51
#use this for installation: 
#pip install torch==2.5.1+cu118 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu118

#for cuda 12x use torch 2.51 and torchaudio 2.51
#use this for installation:
# pip install torch==2.5.1+cu121 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# dont forget to install cudnn for your version of cuda

#or in you got powerful cpu in line 52 switch from cuda to cpu

ARABIC_CHARS_REGEX = re.compile(r'[\u0600-\u06FF]')

def reshape_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def is_arabic(text):
    return bool(ARABIC_CHARS_REGEX.match(text))

async def process_text(recorded_text, log):
    if is_arabic(recorded_text):
        reshaped_text = reshape_arabic_text(recorded_text)
        print(f"Recorder Output (Arabic): {reshaped_text}")
        log.append(reshaped_text)
    else:
        print(f"Recorder Output: {recorded_text}")
        log.append(recorded_text)

async def recorder_and_recognizer(log, recorder):
    try:
        recorded_text = recorder.text()
        await process_text(recorded_text, log)
    except Exception as e:
        print(f"Error with AudioToTextRecorder: {e}")
    return log

async def main_stt():
    log =[]
    with AudioToTextRecorder(model="tiny", device="cuda",compute_type="float32") as recorder:
        log = await recorder_and_recognizer(log, recorder)
        await asyncio.sleep(0.005)

    return "\n".join(log)




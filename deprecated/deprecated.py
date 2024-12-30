


import arabic_reshaper  # Handles reshaping of Arabic text for proper display
import re  # Provides regular expression support
from bidi.algorithm import get_display


def arabic():
        if is_arabic(recorded_text):  # Check if the text is Arabic
        reshaped_text = reshape_arabic_text(recorded_text)  # Reshape Arabic text
        print(f"Recorder Output (Arabic): {reshaped_text}")  # Display reshaped Arabic text
        log.append(reshaped_text)  # Add reshaped text to the log
        else:
        print("stuff")



def is_arabic(text):
    """
    Checks if the given text contains Arabic characters.
    Returns True if the text is Arabic, otherwise False.
    """
    return bool(ARABIC_CHARS_REGEX.match(text)) 





ARABIC_CHARS_REGEX = re.compile(r'[\u0600-\u06FF]')

def reshape_arabic_text(text):
    """
    Reshapes Arabic text for proper display by reshaping characters
    and applying bidirectional algorithm for alignment.
    """
    reshaped_text = arabic_reshaper.reshape(text)  # Reshape Arabic characters for rendering
    bidi_text = get_display(reshaped_text)  # Apply bidirectional text formatting
    return bidi_text
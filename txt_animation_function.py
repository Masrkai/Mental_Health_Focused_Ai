import time 


def print_animated_txt(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()


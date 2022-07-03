import os
from time import time

import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks


def generate_folder() -> str:
    folder: str = f'{os.getcwd()}/{str(int(round(time() * 1000)))}'
    return folder


def split_audio_in_chunks(source: str, max_length: int = 30000) -> tuple[list, str]:
    sound = AudioSegment.from_mp3(source)
    chunks: list = make_chunks(sound, max_length)
    chunks_filenames: list = []
    # Create folder with source name
    folder: str = generate_folder()
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i, chunk in enumerate(chunks):
        filename: str = f'{folder}/chunk_{i}.wav'
        chunk.export(filename, format="wav")
        chunks_filenames.append(filename)
    return chunks_filenames, folder


def convert_speech_to_text(source: str, language: str = 'fr-FR') -> str:
    files, folder = split_audio_in_chunks(source)
    text: str = ""
    r: sr.Recognizer = sr.Recognizer()
    for file in files:
        with sr.AudioFile(file) as source:
            audio = r.listen(source)
            try:
                text += ' ' + r.recognize_google(audio, language=language)
            except sr.UnknownValueError:
                print(f"Could not recognize {file}")
            except Exception as e:
                print(f"Error: {e}")

    for file in files:
        if os.path.exists(file):
            os.remove(file)
    if os.path.exists(folder):
        os.rmdir(folder)
    return text

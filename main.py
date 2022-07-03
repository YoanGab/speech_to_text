import sys
from os import path

from pydub import AudioSegment
from pydub.utils import make_chunks

import file_conversion
import speech_to_text


def convert_mp3_to_wav(source: str, destination: str):
    sound = AudioSegment.from_mp3(source)
    sound.export(destination, format="wav")


def split_audio_in_chunks(source: str, max_length: int = 30000) -> None:
    sound = AudioSegment.from_mp3(source)
    chunks: list = make_chunks(sound, max_length)
    for i, chunk in enumerate(chunks):
        print(f'Chunk {i}')
        filename: str = f'{path.splitext(source)[0]}_chunk_{i}.wav'
        chunk.export(filename, format="wav")
        print(f'Chunk {i} exported to {filename}')


def main():
    source: str = sys.argv[1]
    if source.endswith(".mp3"):
        file_conversion.convert_mp3_to_wav(source)
        source = source.replace('.mp3', '.wav')
    elif not source.endswith(".wav"):
        raise Exception("File type not supported")

    text: str = speech_to_text.convert_speech_to_text(source)
    with open(source.replace('.wav', '.txt'), 'w') as f:
        f.write(text)


if __name__ == '__main__':
    main()

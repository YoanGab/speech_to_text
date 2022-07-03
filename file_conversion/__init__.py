from pydub import AudioSegment


def convert_mp3_to_wav(source: str) -> None:
    """
    Converts an mp3 file to a wav file.
    :param source: The source file.
    :return: None
    """
    if not source.endswith('.mp3'):
        return
    sound = AudioSegment.from_mp3(source)
    destination: str = source.replace(".mp3", ".wav")
    sound.export(destination, format="wav")

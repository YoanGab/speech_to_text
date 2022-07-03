import os
from time import time

from flask import Blueprint, render_template, request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import file_conversion
import speech_to_text

views = Blueprint('views', __name__)


def save_file(file: FileStorage) -> str:
    folder: str = 'uploads'
    filename: str = secure_filename(file.filename)
    timestamp: str = str(int(round(time() * 1000)))
    file_path: str = os.path.join(folder, f"{timestamp}_{filename}")
    file.save(file_path)
    return file_path


@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if 'file' not in request.files:
        return render_template('index.html')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html')

    # Check if file is .mp3 or .wav, if it is save it to the uploads folder
    if not file.filename.endswith('.mp3') and not file.filename.endswith('.wav'):
        return render_template('index.html')

    filename: str = save_file(file)
    # Convert the file to .wav
    file_conversion.convert_mp3_to_wav(filename)

    language: str = request.form['language']
    # Transcribe the file
    file_path: str = filename.replace('.mp3', '.wav')
    transcription: str = speech_to_text.convert_speech_to_text(file_path, language)
    # Delete the .wav file
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(filename):
        os.remove(filename)

    return render_template('index.html', transcription=transcription)


@views.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@views.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

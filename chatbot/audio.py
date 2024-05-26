import subprocess
import speech_recognition as sr
from gtts import gTTS

def convert_webm_to_wav(webm_path, wav_path):
    command = ['ffmpeg', '-y', '-i', webm_path, wav_path]
    subprocess.run(command, check=True)

def audio_to_text(file_path):
    recognizer = sr.Recognizer()
    wav_path = 'donusturulmus_ses.wav'
    convert_webm_to_wav(file_path, wav_path)
    
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio, language='tr-TR')
    return text

def text_to_speech(text, audio_path):
    tts = gTTS(text=text, lang='tr')
    tts.save(audio_path)

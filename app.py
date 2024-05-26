from flask import Flask, render_template, request, jsonify, send_from_directory
from chatbot import gpt, audio, data_loader
from chatbot.cache import Cache
import openai
import logging
import os
from gtts import gTTS

app = Flask(__name__)
cache = Cache(expiration_time=3600)  # 1 saatlik önbellek süresi

data = data_loader.load_data('chatbot/data.json')
if data is None:
    raise Exception("Failed to load data.json")

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

logging.debug(f"Loaded data: {data}")

def shorten_response(response, max_length=150):
    if len(response) > max_length:
        end_idx = response.rfind('. ', 0, max_length)
        if end_idx == -1:
            end_idx = response.rfind(' ', 0, max_length)
        if end_idx == -1:
            return response[:max_length] + '...'
        return response[:end_idx + 1] + '...'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    logging.debug(f"Kullanıcı girişi: {user_input}")

    answer = data_loader.find_answer(data, user_input)
    logging.debug(f"JSON'dan yanıt: {answer}")

    if answer:
        response = answer
    else:
        cached_response = cache.get(user_input)
        logging.debug(f"Önbellekteki yanıt: {cached_response}")

        if cached_response:
            response = cached_response
        else:
            try:
                gpt_response = gpt.get_response(user_input)
                response = shorten_response(gpt_response)
                logging.debug(f"GPT'den yanıt: {response}")
                cache.set(user_input, response)
            except openai.error.RateLimitError as e:
                logging.error(f"API çağrı limiti hatası: {e}")
                response = "Üzgünüm, API çağrı limitime ulaştım. Lütfen daha sonra tekrar deneyin."
            except openai.error.OpenAIError as e:
                logging.error(f"OpenAI API hatası: {e}")
                response = "İsteğinizi işlerken bir hata oluştu. Lütfen daha sonra tekrar deneyin."

    audio_file = "yanit.mp3"
    audio_path = os.path.join('deneme13', audio_file)
    tts = gTTS(text=response, lang='tr')
    tts.save(audio_path)

    return jsonify({'text': response, 'audio': '/yanit.mp3'})

@app.route('/voice_chat', methods=['POST'])
def voice_chat():
    audio_data = request.files['audio']
    file_path = 'yuklenen_ses.webm'
    audio_data.save(file_path)

    try:
        text = audio.audio_to_text(file_path)
        logging.debug(f"Metne dönüştürülen ses: {text}")

        answer = data_loader.find_answer(data, text)
        logging.debug(f"JSON'dan yanıt: {answer}")

        if answer:
            response = answer
        else:
            cached_response = cache.get(text)
            logging.debug(f"Önbellekteki yanıt: {cached_response}")

            if cached_response:
                response = cached_response
            else:
                try:
                    gpt_response = gpt.get_response(text)
                    response = shorten_response(gpt_response)
                    logging.debug(f"GPT'den yanıt: {response}")
                    cache.set(text, response)
                except openai.error.RateLimitError as e:
                    logging.error(f"API çağrı limiti hatası: {e}")
                    response = "Üzgünüm, API çağrı limitime ulaştım. Lütfen daha sonra tekrar deneyin."
                except openai.error.OpenAIError as e:
                    logging.error(f"OpenAI API hatası: {e}")
                    response = "İsteğinizi işlerken bir hata oluştu. Lütfen daha sonra tekrar deneyin."

        audio_file = "yanit.mp3"
        audio_path = os.path.join('deneme13', audio_file)
        tts = gTTS(text=response, lang='tr')
        tts.save(audio_path)

        return jsonify({'text': response, 'audio': '/yanit.mp3'})
    finally:
        os.remove(file_path)  # Geçici dosyayı kaldır

@app.route('/yanit.mp3')
def serve_audio():
    return send_from_directory(directory='deneme13', path='yanit.mp3')

if __name__ == '__main__':
    app.run(debug=True)

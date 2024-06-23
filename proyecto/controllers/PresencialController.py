import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import threading
import queue
import os

recognizer = sr.Recognizer()
translator = Translator()

voice_queue = queue.Queue()

def get_available_languages():
    return LANGUAGES

def voice_worker():
    while True:
        text = voice_queue.get()
        if text is None:
            break
        tts = gTTS(text, lang='en')  # Ajusta el idioma según tus necesidades
        audio_path = f'uploads/translation_current.mp3'
        tts.save(audio_path)
        os.system(f"mpg123 {audio_path}")
        voice_queue.task_done()

voice_thread = threading.Thread(target=voice_worker)
voice_thread.daemon = True
voice_thread.start()

def recognize_and_translate(source_lang, target_lang, shared_data):
    error_message = None

    def capture_audio_thread(shared_data):
        nonlocal error_message

        with sr.Microphone() as source:
            print("Speak now...")
            while shared_data["capture_audio"]:
                try:
                    audio = recognizer.listen(source, timeout=5)

                    if audio is not None:
                        text = recognizer.recognize_google(audio, language=source_lang)
                        shared_data['recognized_texts'].append(text)

                        translation = translator.translate(text, dest=target_lang).text
                        shared_data['translation_texts'].append(translation)
                        print("You said: {}".format(text))
                        print("Translation: {}".format(translation))

                        # Verificar y crear la carpeta 'uploads' si no existe
                        if not os.path.exists('uploads'):
                            os.makedirs('uploads')

                        # Guardar la traducción como archivo de audio
                        translation_audio = gTTS(translation, lang=target_lang)
                        audio_path = f'uploads/translation_{len(shared_data["translation_texts"])}.mp3'
                        translation_audio.save(audio_path)

                        # Verificar si el archivo de audio se ha guardado correctamente
                        if not os.path.exists(audio_path):
                            print("El archivo de audio no se ha guardado correctamente.")
                        else:
                            print("El archivo de audio se ha guardado correctamente en", audio_path)
                            shared_data['audio_path'] = audio_path
                            shared_data['audio_processed'].append(audio_path)  # Añadir a los procesados

                        # Enqueue the translation for speaking
                        if shared_data.get("speak_translations", False):
                            voice_queue.put(translation)

                except sr.UnknownValueError:
                    print("Sorry! Could not understand audio.")
                except sr.RequestError as e:
                    print("Error with the request; {0}".format(e))
                except Exception as e:
                    print("Error: {0}".format(e))

    return capture_audio_thread, error_message


import os
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer
from argostranslate import translate

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
VOSK_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'vosk-model-es-0.42')

def convertir_audio_compatible(input_path, output_path):
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', input_path,
            '-ac', '1',
            '-ar', '16000',
            '-sample_fmt', 's16',
            output_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir el audio: {e}")
        return False

def transcribir_audio_offline(filename):
    if not os.path.exists(VOSK_MODEL_PATH):
        raise FileNotFoundError(f"Modelo Vosk no encontrado en: {VOSK_MODEL_PATH}")

    model = Model(VOSK_MODEL_PATH)

    # Ruta del audio original
    audio_path = os.path.join(UPLOAD_FOLDER, filename)

    # Ruta del archivo convertido
    audio_convertido = os.path.join(UPLOAD_FOLDER, "temp_audio.wav")

    # Convertir a formato compatible
    if not convertir_audio_compatible(audio_path, audio_convertido):
        return "Error: No se pudo convertir el archivo de audio."

    try:
        wf = wave.open(audio_convertido, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            return "Error: El audio convertido aún no cumple el formato WAV mono PCM 16 bits."

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        resultado_final = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                resultado_final += result.get("text", "") + " "

        final_result = json.loads(rec.FinalResult())
        resultado_final += final_result.get("text", "")

        wf.close()
        os.remove(audio_convertido)  # Limpieza

        return resultado_final.strip()
    except Exception as e:
        print(f"Error durante la transcripción: {str(e)}")
        return f"Error: No se pudo transcribir el audio. {str(e)}"

def traducir_offline(texto, origen="es", destino="en"):
    try:
        print(f"Traduciendo texto de {origen} a {destino}")
        print(f"Texto original: {texto[:50]}...")

        installed_languages = translate.get_installed_languages()
        print(f"Idiomas instalados: {[lang.code for lang in installed_languages]}")

        from_lang = next((lang for lang in installed_languages if lang.code == origen), None)
        to_lang = next((lang for lang in installed_languages if lang.code == destino), None)

        if not from_lang:
            return f"Error: Idioma de origen '{origen}' no está instalado."
        if not to_lang:
            return f"Error: Idioma de destino '{destino}' no está instalado."

        translation = from_lang.get_translation(to_lang)
        if not translation:
            return f"Error: No hay traducción disponible de '{origen}' a '{destino}'."

        resultado = translation.translate(texto)
        print(f"Traducción completada: {resultado[:50]}...")
        return resultado
    except Exception as e:
        print(f"Error en la traducción: {str(e)}")
        return f"Error: No se pudo traducir el texto. {str(e)}"

import os
from pydub import AudioSegment
import speech_recognition as sr

async def convert_text(audio_file):
        converted_audio_file = "audio.wav"
        audio = AudioSegment.from_ogg(audio_file)
        audio.export(converted_audio_file, format="wav")

        # Создайте объект распознавания
        recognizer = sr.Recognizer()

        # Распознавание речи
        with sr.AudioFile(converted_audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language='ru-Ru')  # Можете выбрать другой recognizer
                print("Распознанный текст из голосового сообщения:", text)
            except sr.UnknownValueError:
                print("Речь не распознана")
            except sr.RequestError as e:
                print(f"Ошибка при запросе к сервису распознавания речи: {e}")
        os.remove(converted_audio_file)
        return text

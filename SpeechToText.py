import speech_recognition


def recognize_speech(path, language):
    recognizer = speech_recognition.Recognizer()
    audio = speech_recognition.AudioFile(path)
    with audio as audio_for_recording:
        recorded_audio = recognizer.record(audio_for_recording)
    return recognizer.recognize_google(recorded_audio, language = language)
import whisper
import pyttsx3
import sounddevice as sd
import wave
import os

# Initialisation du modèle Whisper
model = whisper.load_model("base")  # Modèles disponibles : "tiny", "base", "small", "medium", "large"

# Initialisation du moteur Text-to-Speech (TTS)
engine = pyttsx3.init()

# Fonction pour enregistrer l'audio depuis le microphone avec SoundDevice
def record_audio(output_file="temp_audio.wav", duration=5, samplerate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Attendre la fin de l'enregistrement
    print("Recording finished.")

    # Sauvegarder les données audio dans un fichier WAV
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 octets (16 bits) par échantillon
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

# Fonction pour convertir l'audio en texte avec Whisper
def speech_to_text(audio_file):
    print("Transcribing audio with Whisper...")
    result = model.transcribe(audio_file, language="fr")
    return result["text"]

# Fonction pour convertir le texte en audio avec pyttsx3
def text_to_speech(text):
    print("Synthesizing speech...")
    engine.say(text)
    engine.runAndWait()

# Fonction principale pour le pipeline Speech-to-Speech
def main():
    try:
        # Étape 1 : Enregistrement de l'audio
        audio_file = "temp_audio.wav"
        record_audio(output_file=audio_file, duration=5)  # Enregistrement de 5 secondes

        # Étape 2 : Transcription avec Whisper
        text = speech_to_text(audio_file)
        print(f"Recognized text: {text}")

        # Étape 3 : Synthèse vocale du texte transcrit
        text_to_speech(text)

        # Nettoyage du fichier temporaire
        if os.path.exists(audio_file):
            os.remove(audio_file)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

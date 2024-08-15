from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import pyttsx3
from langdetect import detect
import pycountry

# Function to speak text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to get language name from language code
def getLangName(lang_code):
    language = pycountry.languages.get(alpha_2=lang_code)
    return language.name if language else "Unknown"

# Function to capture voice command
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"The User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

# Function to detect destination language
def destination_language():
    print("Enter the language in which you want to convert: Ex. Hindi, English, Spanish, etc.")
    to_lang = takecommand()
    while to_lang == "None":
        to_lang = takecommand()
    to_lang = to_lang.lower()
    return to_lang

if __name__ == "__main__":
    # Initialize pyttsx3 engine
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    print("Welcome to the translator!")
    speak("Welcome to the translator!")
    print("Say the sentence you want to translate once you see the word 'Listening'")

    query = takecommand()
    while query == "None":
        query = takecommand()

    from_lang = detect(query)
    print(f"The user's sentence is in {getLangName(from_lang)}")

    to_lang = destination_language()

    # Convert to_lang to valid gTTS language code
    gTTS_lang_code = {
        'english': 'en',
        'hindi': 'hi',
        'spanish': 'es',
        # Add more languages as needed
    }

    if to_lang in gTTS_lang_code:
        gTTS_code = gTTS_lang_code[to_lang]
    else:
        print(f"Language '{to_lang}' not supported for translation.")
        exit()

    # Translate using Google Translate
    translator = Translator()
    text_to_translate = translator.translate(query, dest=gTTS_code)
    translated_text = text_to_translate.text

    # Speak the translated text
    speak_tts = gTTS(text=translated_text, lang=gTTS_code, slow=False)
    speak_tts.save("translated_audio.mp3")
    playsound("translated_audio.mp3")

    # Clean up temporary audio file
    os.remove('translated_audio.mp3')

    print(f"Translated Text: {translated_text}")

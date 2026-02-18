
import speech_recognition as sr  #used for speech recognition
import webbrowser                #used to open web pages
import pyttsx3                   #used for text to speech conversion
import musicLibrary              #importing music library
import requests                  #used to make http requests
from openai import OpenAI        #importing OpenAI client
from gtts import gTTS            #importing Google Text to Speech
import pygame                    #importing Pygame for audio playback
import os                        #importing os to handle file operations

# pip install pocketsphinx

recognizer = sr.Recognizer()       #initialize the recognizer
engine = pyttsx3.init()            #initialize the TTS engine
newsapi = "c56a52da8ee148a8b5412904d166b6f8"   #News API key

def speak_old(text):           #function to convert text to speech using pyttsx3
    engine.say(text)
    engine.runAndWait()

def speak(text):               #function to convert google text to speech using gTTS and play with Pygame
    # Convert text to speech and save as MP3
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():     #wait for music to finish playing
        pygame.time.Clock().tick(10)         #check if music is still playing
    
    pygame.mixer.music.unload()              #unload the music
    os.remove("temp.mp3")                    #remove the temporary file

def ai_process(command):                 #function to process command using OpenAI API  
    client = OpenAI(api_key="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",
    )
     # pip install openai
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content  #return the response from OpenAI

def process_command(c):          #function to process the command i.e open websites, play music, get news or use AI
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):        #play music from music library
        song = c.lower().split(" ")[1]        #get the song name
        link = musicLibrary.music[song]       #get the song link from music library
        webbrowser.open(link)                 #open the song link in web browser

    elif "news" in c.lower():                 #get news headlines using News API
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = ai_process(c)
        speak(output) 




# Initialize the speech recognition and text-to-speech engines
if __name__ == "__main__":            
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yes Boss...")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Actived...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    process_command(command)


        except Exception as e:
            print("Error; {0}".format(e))

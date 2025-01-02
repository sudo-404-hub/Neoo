import speech_recognition as sr 
import pyttsx3
import webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()


def user_voice_input():
    while True:
        r = sr.Recognizer()  # Create a Recognizer instance to recognize speech
        with sr.Microphone() as source:  # Use the default microphone as the audio source
            print("Please say something...")  # Prompt the user to speak
            r.pause_threshold = 2  # Set the pause threshold to 2 seconds
            
            # Adjust for ambient noise to improve recognition accuracy
            r.adjust_for_ambient_noise(source)
            
            
            try:
                # Listen for audio input from the microphone
                audio = r.listen(source)
                
                # Use Google Web Speech API to convert audio to text
                query = r.recognize_google(audio, language="en-in") 
                print(query)

                # search on google
                if "alexa search" in query.lower():
                    print(f"searching: {query}")
                    webbrowser.open(f'https://www.google.com/search?q={query[13:]}')

                # search on google
                if "alexa youtube" in query.lower():
                    print(f"searching: {query}")
                    webbrowser.open(f'https://www.youtube.com/search?q={query[14:]}')

                # convert input into speech
                engine.say(query) 
                engine.runAndWait()

            except sr.UnknownValueError:
                # Handle the case where speech is unintelligible
                print("Sorry, I could not understand your speech. Please try again.")
                return None
            except sr.RequestError as e:
                # Handle issues with the Google Speech API (e.g., no internet)
                print("You are not connected to internet")
                return None

user_voice_input()

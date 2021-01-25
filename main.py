import speech_recognition as sr
import pyttsx3
import datetime
import time
import geocoder
from spotify import *

#Spotify
client_id = 'your client_id'
client_secret = 'your client_secret'

#Location
myloc = geocoder.ip('me')

#Speech
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Weather
api_key = "your api_key"
lat = myloc.lat
lon = myloc.lng
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

def getWeather():
    response = requests.get(url)
    data = json.loads(response.text)
    temp = data["current"]["temp"]
    desc = data["current"]["weather"][0]["description"]
    feels_like = data["current"]["feels_like"]
    return temp, desc, feels_like

def getDateTime():
    day = datetime.date.today()
    time = datetime.datetime.now()
    current_day = day.strftime("%B %d, %Y")
    current_time = time.strftime("%H:%M")
    return current_day, current_time

def getName(name):
    return name

# Function to reply a given string
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to your commands
def detect_command():
    with sr.Microphone() as source:
        print('listening...')
        voice = listener.listen(source)
        try:
            command = listener.recognize_google(voice)
            command = command.lower()
            #print(command)
        except:
            talk('Sorry, I did not understand that. Please repeat')
            detect_command()
        return command

def respond(command):
    if 'hello' in command:
        talk(f'hello {getName("...")}')
    elif 'weather' in command:
        temp = str(round(getWeather()[0], 1))
        desc = str(getWeather()[1])
        feels_like = str(round(getWeather()[2], 1))
        talk(f'It is {desc}. The temperature is {temp} degrees, but it feels like {feels_like} degrees.')
    elif 'day' in command:
        day = getDateTime()[0]
        print(day)
        talk(f'Today is {day}')
    elif 'time' in command:
        time = getDateTime()[1]
        print(time)
        talk(f'The time is {time}')
    elif 'play' in command:
        spotify = SpotifyAPI(client_id, client_secret)
        spotify.get_access_token()
        print(command.split(' ')[1])
        spotify.play_track(command.split(' ')[1])
        exit()
    elif 'playlist' in command:
        spotify = SpotifyAPI(client_id, client_secret)
        spotify.get_access_token()
        playlist = spotify.get_playlist('7CBEk98HK4dBR1XJChx3ZW')  # Insert the playlistID of the playlist you want to open
        webbrowser.open(playlist['external_urls']['spotify'])  # Opens the playlist in your browser.
        # You have to manually press the play button to play the songs.
        exit()
    elif 'exit' in command:
        exit()
        # Stops the program from listening


time.sleep(1)
#talk("How can i help you")
while 1:
    command = detect_command()
    respond(command)

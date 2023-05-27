#Importing Libraries
import datetime
import sys

import requests, json
from sys import exit
import pyjokes
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia

listener = sr.Recognizer()
#Define our engine bot with women voice
engine = pyttsx3.init()
voices =engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)


def engine_talk(text):
    engine.say(text)
    engine.runAndWait()


def weather(city):
    #using an API to get the weather
    api_key = "50b1bdc5ae822a743f7443fa0a9c6a1d"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    #get the url and our api
    #with &q it will get the city weather
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        return str(current_temperature)
        print(" Temperature (in kelvin unit) = " +
              str(current_temperature) +
              "\n description = " +
              str(weather_description))
    else:
        print(" City Not Found ")

#with user_command our user use microphone to talk with engine
def user_commands():
    try:
        with sr.Microphone() as source:
            print("Start Speaking!!")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)

    except:
        pass
    return command


def run_alexa():
    command = user_commands()
    if 'play' in command:
        song = command.replace('play', '')
        #print('Your New command is:' +command)
        #print('the bot is telling us: playing' +command)
        engine_talk('Playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
       time = datetime.datetime.now().strftime('%I:%M %p')
       engine_talk('The Current time is' + time)
    elif 'who is' in command:
       name = command.replace('who is', '')
       info = wikipedia.summary(name)
       print(info)
       engine_talk(info)
    elif 'hello' in command:
        engine_talk('hi dear')
    elif 'how are you doing' in command:
        engine_talk('i am totally fine, what do you need?')
    elif 'joke' in command:
       engine_talk(pyjokes.get_joke())
    elif 'weather' in command:
        engine_talk('Please tell the name of the city')
        city = user_commands()
        weather_api = weather(city)
        engine_talk(weather_api + 'degree fahreneit')


    elif 'stop' in command:
        sys.exit()

    else:
        engine_talk('i could not hear you properly')

while True:
    run_alexa()

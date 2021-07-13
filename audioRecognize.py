import speech_recognition as sr
import os
import smtplib
import translate
import datetime
from email.mime.text import MIMEText
from tkinter import filedialog
from tkinter import simpledialog

rec=None
audio=None
result=None
text=None

def listen_using_microphone():
    global rec
    rec = sr.Recognizer()
    # It will create object of the class Recognizer present in speech_recognition module
    with sr.Microphone() as source:
        print("Speak Something :")
        global audio
        audio = rec.listen(source)
        # listen function will start listening and will stop automatically when audio stops coming


def listen_from_audiofile():
    global rec
    rec = sr.Recognizer()
    file_name = filedialog.askopenfile(filetypes=[("All Files", "*.*"),
                                              ("Audio file", "*.wav")])
    file_name = file_name.name

    with sr.AudioFile(file_name) as source:
        global audio
        audio = rec.record(source)


def recognize_audio():
    global text
    text = rec.recognize_google(audio) # it will convert listened audio to text using google api

    print("You Said :",text)
    return text


def translate_to_hindi():
    trans = translate.Translator(to_lang = 'hi')
     # It will create object of the class Translator present in translate module
    global result
    result = trans.translate(text)
     # It will translate the given text to given language

    print("Translation : ",result)
    return result




if __name__ == "__main__":
    input_as_audio_file = input("Do you want to give input as audio file (y/n):")
    if(input_as_audio_file.lower()=='y'):
        listen_from_audiofile()
    else:
        listen_using_microphone()

    recognize_audio()
    translate_to_hindi()


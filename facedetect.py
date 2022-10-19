# Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
from imutils import face_utils
import random
import beepy
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyjokes


def activate():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    print(voices)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 120)

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    def wishMe():
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak("Good Morning!")
        elif hour >= 12 and hour <= 18:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")
        speak("Sir ,you are sleepy...., Let me know how can I entertain you? ")

    def takeCommand():
        # microphone input and returns string output
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening to you ......")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            speak("Sorry , i didnt get you, Can you say that again please")
            print("Sorry , i didnt get you, Can you say that again please")
            return "None"
        return query

    def sendEmail(to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('hemanthmodani2001@gmail.com', '****')
        server.sendmail('hemanthmodani2001@gmail.com', to, content)
        server.close()

    wishMe()
    while True:
        query = takeCommand().lower()
        # logics begins here
        if 'wikipedia' in query:
            speak("Searching Wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(results)
            print(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'play music' in query:
            music_dir = 'C:\music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sir , the time is {strTime}")
        elif 'who created you' in query:
            speak('Rollnos 10 30 31 63 65 of B5 section created me')
        elif 'email' in query:
            try:
                speak("What should i say?")
                content = takeCommand()
                to = "121910305063@gmail.com"
                sendEmail(to, content)
                speak('email has been sent')
            except Exception as e:
                print(e)
                speak('sorry email is not sent')
        elif 'joke' in query:
            My_joke = pyjokes.get_joke(language="en", category="neutral")
            speak(My_joke)
            print(My_joke)
        elif 'dialogue' in query:
            l = ['Kottanu antey medical testlu cheyinchukotaniki nee asthulu ammina saripovu', 'Okadu Naa Mundu Action Cheste Enjoy Chesta … Over Action Cheste Injure Chestha',
                 'Prabhuthvam tho pani cheinchukoavadam mana hakkuu.danni lancham tho konnodhu', 'If one do action in front me? I Enjoy. If One Do overaction, I Injure', 'Maadi rayalasimanna ammathodu entamandosthe anthamandini addanga narikesta']

            s = random.randint(0, len(l)-1)
            speak(l[s])
        



# Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)

# Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# status marking for current state
sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)


def compute(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist


def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up/(2.0*down)

    # Checking if it is blinked
    if (ratio > 0.25):
        return 2
    elif (ratio > 0.21 and ratio <= 0.25):
        return 1
    else:
        return 0


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    # detected face in faces array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # The numbers are actually the landmarks which will show eye
        left_blink = blinked(landmarks[36], landmarks[37],
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43],
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Now judge what to do for the eye blinks
        if (left_blink == 0 or right_blink == 0):
            sleep += 1
            drowsy = 0
            active = 0
            if (sleep > 50):
                status = "SLEEPING !!!"
                color = (255, 0, 0)
                activate()

        elif (left_blink == 1 or right_blink == 1):
            sleep = 0
            active = 0
            drowsy += 1
            if (drowsy > 10):
                status = "Drowsy !"
                color = (0, 0, 255)

        else:
            drowsy = 0
            sleep = 0
            active += 1
            if (active > 10):
                status = "Active :)"
                color = (0, 255, 0)

        cv2.putText(frame, status, (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

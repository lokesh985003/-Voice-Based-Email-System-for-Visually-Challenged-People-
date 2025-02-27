import speech_recognition as sr
import easyimap as e
import pyttsx3
import smtplib
import difflib  


EMAIL = "subscriberno.3tinku@gmail.com"
PASSWORD = "dzrc lrsl aahp xwsa"


recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[1].id)  
engine.setProperty('rate', 150)  

def speak(text):
    """Text-to-Speech Output"""
    print("[Assistant]:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures speech and returns recognized text"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=3)
        speak("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            recognized_text = recognizer.recognize_google(audio, language="en-US").lower().strip()
            print("[Recognized]:", recognized_text)
            return recognized_text
        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said.")
            return None
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
            return None
        except sr.WaitTimeoutError:
            speak("No speech detected. Please try again.")
            return None

def interpret_command(command_text):
    """
    Interprets the spoken command and returns one of:
    'send', 'read', or 'exit'
    """
    if command_text is None:
        return None
    command_text = command_text.lower()
    
    if "send" in command_text:
        return "send"
    elif "read" in command_text:
        return "read"
    elif "exit" in command_text or "quit" in command_text:
        return "exit"
    else:
        
        possible = ["send", "read", "exit"]
        match = difflib.get_close_matches(command_text, possible, n=1, cutoff=0.6)
        return match[0] if match else None

def send_mail():
    """Send an email via Gmail"""
    recipient = "9921004517@klu.ac.in"  
    speak("Please speak the body of your email. For example, 'please send an email' followed by your message.")
    message = listen()
    if not message:
        speak("No message received. Email not sent.")
        return
    speak("You said: " + message)
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        
        server.sendmail(EMAIL, recipient, f"Subject: Voice Email\n\n{message}")
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Failed to send email.")
        print("Error:", e)

def read_mail():
    """Read the latest 3 emails from your inbox"""
    try:
        server = e.connect("imap.gmail.com", EMAIL, PASSWORD)
        mail_ids = server.listids()
        if not mail_ids:
            speak("No emails found in your inbox.")
            return
        speak("Reading the latest emails:")
        
        for i in range(min(3, len(mail_ids))):
            email = server.mail(mail_ids[i])
            speak("Email number " + str(i+1))
            speak("From: " + email.from_addr)
            speak("Subject: " + email.title)
            speak("Body: " + email.body)
    except Exception as e:
        speak("Could not fetch emails.")
        print("Error:", e)


speak("Welcome!")
while True:
    speak("What do you want to do? Say 'send an email' to send mail, 'read inbox' to read your emails, or 'exit' to quit.")
    command = listen()
    interpreted = interpret_command(command)
    print("[Interpreted Command]:", interpreted)
    if interpreted == "send":
        send_mail()
    elif interpreted == "read":
        read_mail()
    elif interpreted == "exit":
        speak("Exiting the program. Goodbye!")
        break
    else:
        speak("Sorry, I did not understand. You said: " + str(command))

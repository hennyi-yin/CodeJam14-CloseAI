import speech_recognition as sr

def real_time_speech_to_text():
    text = ''
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    #print("Adjusting for ambient noise... Please wait.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Speak into the microphone.")
        while True:
            try:
                # Capture audio from the microphone
                audio = recognizer.listen(source, timeout=20)
                
                # Convert speech to text using Google Web Speech API
                text = recognizer.recognize_google(audio)
                return text
            except Exception as e:
                pass
           

# Run the function
#print(real_time_speech_to_text())

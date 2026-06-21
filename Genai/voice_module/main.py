import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Speak now...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)

except sr.UnknownValueError:
    print("❌ Could not understand audio")

except sr.RequestError as e:
    print("❌ API request failed:", e)

except Exception as e:
    print("❌ Error:", e)
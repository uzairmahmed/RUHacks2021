from gtts import gTTS
import os

testText = "test hello ooga booga"

def tts(text, lang ='en'):
    output = gTTS(text=text, lang=lang, slow=False)
    output.save("ttsFile.mp3")

tts(testText)
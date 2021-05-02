from gtts import gTTS
import os

def text_to_speech(text, lang ='en'):
    output = gTTS(text=text, lang=lang, slow=False)
    output.save("ttsFile.mp3")

#testText = "test hello"
#tts(testText)
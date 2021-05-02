from gtts import gTTS
import os

def tts(text, lang ='en'):
    output = gTTS(text=text, lang=lang, slow=False)
    output.save("ttsFile.mp3")

#testText = "test hello ooga booga"
#tts(testText)
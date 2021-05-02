import os, six
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"./google_keys.json"
# See https://g.co/cloud/translate/v2/translate-reference#supported_languages


def translate_text(target, text):
    """
    translates text. 
    target: 2 letter language code (look at get_langs)
    text: self explanatory
    """
    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    return "\"" + result["input"] + "\" (" + result["detectedSourceLanguage"] \
        + ")\n\"" + result["translatedText"] + "\" (" + target + ")\n"

def get_langs():
    """
    returns googles supported translate languages. 
    """
    temp = ""
    translate_client = translate.Client()
    for i in translate_client.get_languages():
        temp += i['name'] + ": " + i['language'] + "\n"

    return temp

def tests():
    text = "bonjour mon nom est arjun et je suis une salope stupide"
    lang = "en"
    print("Translate: " + translate_text(lang, text))

#tests()
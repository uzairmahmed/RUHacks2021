import os, six
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"./google_keys.json"
# See https://g.co/cloud/translate/v2/translate-reference#supported_languages
translate_client = translate.Client()

def translate_text(target, text):

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


print(translate_client.get_languages())
# print(translate_text())
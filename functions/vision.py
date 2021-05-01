import os, io
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"./google_keys.json"

def ocr(url):
    """
    runs OCR on an image and returns the text from it
    url: discord media url from the command invocation message
    """
    client = vision.ImageAnnotatorClient()
    
    image = vision.Image()
    image.source.image_uri = url

    response = client.text_detection(image=image)

    texts = response.text_annotations
    if response.error.message:
        return response.error.message
    else:
        return texts[0].description


def identify(url):
    """
    runs object detection on an image and returns a list of all detected objects in it
    url: discord media url from the command invocation message
    """
    objectsList = []
    
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = url

    objects = client.object_localization(
        image=image).localized_object_annotations

    for object_ in objects:
        objectsList.append(object_.name)

    return str(objectsList)

def tests():
    ricoImgURL = 'https://media.discordapp.net/attachments/837958218981703690/838109079259316255/2020-10-13_9.png'

    print("OCR: "       + ocr(ricoImgURL))
    print("Identify: "  + identify(ricoImgURL))

tests()
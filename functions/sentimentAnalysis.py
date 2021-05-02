from google.cloud import language_v1

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient.from_service_account_json(r"./google_keys.json")
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(request={'document': document})
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    return score, magnitude

#score, magnitude=analyze_sentiment("i luv u")
#print(score)
#print(magnitude)

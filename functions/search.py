import os, json
from googleapiclient.discovery import build

with open('more_keys.json', 'r') as f:
    keys = json.load(f)
    f.close()

cse_key = keys["google_cse_key"]
cse_id = keys["google_cse_id"]

def search(query, num_results):
    """
    returns a list of search results as URLs
    query: self explanatory
    num_results: how many URLs u want to send
    """

    temp = []
    service = build("customsearch", "v1", developerKey=cse_key)
    results = service.cse().list(q=query, cx=cse_id).execute()['items']
    for i in range(0, num_results):
        temp.append(results[i]['link'])
    return temp

def image_search(query):
    """
    returns a list of image URLs.
    query: self explanatory
    """

    temp = []
    service = build("customsearch", "v1", developerKey=cse_key)
    results = service.cse().list(q=query, cx=cse_id, searchType = "image").execute()['items']
    print(results)
    
    for i in range(0, len(results)):
        temp.append(results[i]['link'])
    return temp
    
print(search("holy panda", 2))
print(image_search("holy panda"))

import requests
import json


def getImageCaption(image_url):

    headers = {
        'api-key': '0115a598-cfb4-4c3a-b84c-c72ca9af48b1',
    }

    files = {
        'image': (image_url, open(image_url, 'rb')),
    }

    response = requests.post('https://api.deepai.org/api/densecap', headers=headers, files=files,json={"key": "value"})

    resp = json.dumps(response.json()) 
    ans = json.loads(resp)
    return ans['output']['captions'][0]['caption']


textCaption = getImageCaption('/Users/hariharakris/Downloads/surf.jpg')

print(textCaption)

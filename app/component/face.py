import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import io
from PIL import Image

from app import app

def getfaceid(url=None, path=None):
    if (url is None) == (path is None):
        raise ValueError("One of url or path should be set")
    if url is not None:
        contentType = "application/json"
        body = json.dumps({
            'url': url
        })
    else:
        contentType = "application/octet-stream"
        img = Image.open(path) # TODO: handle file exceptions
        output = io.BytesIO()
        img.save(output, format=img.format)
        body = output.getvalue()

    headers = {
        # request headers
        'content-type': contentType,  
        'ocp-apim-subscription-key': app.config["FACE_API_CONFIG"]["KEY"],
    }

    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
    })

    endpoint = app.config["FACE_API_CONFIG"]["ENDPOINTS"]["DETECT"]
    host, path = endpoint["HOST"], endpoint["PATH"]
    conn = http.client.HTTPSConnection(host)
    conn.request("POST", "%s?%s" % (path, params), body, headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    conn.close()
    return data[0]['faceId']

# faceId: query, faceIds: data
# return: list{'faceId' => 'confidience'}
def getConfidenceList(faceId, faceIds):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': app.config["FACE_API_CONFIG"]["KEY"],
    }

    body = {
        'faceId':faceId,
        'faceIds':faceIds,
        "mode": "matchFace"
    }

    params = urllib.parse.urlencode({}) 
    try:
        endpoint = app.config["FACE_API_CONFIG"]["ENDPOINTS"]["FIND_SIMILAR"]
        host, path = endpoint["HOST"], endpoint["PATH"]
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", "%s?%s" % (path, params), json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        list = {}
        for tmp in data:
            list[tmp['faceId']] = tmp['confidence']

        return list

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def aveScore(list, key):
    size = len(list)
    score = 0
    for i in range(0, size):
        score += list[i][key]

    return score/size


def minScore(list, key):
    size = len(list)
    score = 10
    for i in range(0, size):
        if list[i][key] < score:
            score = list[i][key]

    return score

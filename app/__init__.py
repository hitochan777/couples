# Import flask and template operators
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
import urllib
import http
import json

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Configure the image uploading via Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET'])
def search():
    keyword = request.args.get('search-text')
    if keyword is None or len(keyword) == 0:
        return redirect("/", code=302)

    urls = search_images_by_keyword(keyword)

    return render_template('search_result.html', urls=urls)

def search_images_by_keyword(keyword):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': app.config["SEARCH_API_CONFIG"]["KEY"],
    }
    params = urllib.parse.urlencode({
        "q": keyword
    })
    endpoint = app.config["SEARCH_API_CONFIG"]["ENDPOINTS"]["IMAGE_SEARCH"]
    host, path = endpoint["HOST"], endpoint["PATH"]
    conn = http.client.HTTPSConnection(host)
    conn.request("POST", "%s?%s" % (path, params), "", headers)
    response = conn.getresponse()
    raw_data = response.read()
    data = json.loads(raw_data)
    urls = list(map(lambda image: image["contentUrl"], data["value"]))[:3]
    conn.close()
    return urls

# ******************************************************

@app.route("/categorySearch")
def category():
    type = request.args.get('type')
    # if keyword is None or len(keyword) == 0:
    #     return redirect("/", code=302)

    urls = search_category(type)
    return render_template('category.html', urls=urls)

@app.route("/categorySearchFool")
def category_fool():
    type = request.args.get('type')
    # if keyword is None or len(keyword) == 0:
    #     return redirect("/", code=302)

    urls = search_category_fool(type)
    return render_template('category.html', urls=urls)

@app.route("/fujiwaraSearch")
def fujiwara():
    # keyword = request.args.get('search-text')
    # if keyword is None or len(keyword) == 0:
    #     return redirect("/", code=302)

    urls = search_fujiwara()
    return render_template('category.html', urls=urls)

def search_fujiwara():
    querys = [
                'http://eiga.k-img.com/images/person/62515/6d3527baa09166ca/320.jpg',
                'https://mens-cdn.oricon.co.jp/feature/img/0/165/detail/img660/1495702911352.jpg',
                'https://cdn.mdpr.jp/photo/images/5e/fb5/w700c-ez_a3936914fbbf63b7c25a167e6d86d4439aad25000544dde4.jpg',
            ]

    datas = [
                'http://www.takumi-jun.com/contents/upload-images/201458221929.jpg',
                'http://www.isetan-photo.co.jp/sp/shomei/images/recruit_slide04.jpg',
                'http://asakusa-link.com/wp-content/uploads/2016/03/74e3b8ee00cb35feef211ebdc8c76796_s.jpg',
                'http://img01.osakazine.net/usr/s/t/u/studiolib/bst_24135dd.jpg',
                'https://ranking.xgoo.jp/tool/images/column/2016/06/0610_11re.jpg',
                'https://i2.wp.com/nekotopi.com/wp-content/uploads/2014/10/cm-abe.jpg',
                'https://contents.oricon.co.jp/photo/img/0/259/detail/img660/0_84691200_1340881653.jpg',

                'http://i2.w.yun.hjfile.cn/slide/201312/21983267836.jpg',
            ]

    queryFaceIds = {}
    dataFaceIds = []
    idToUrl = {}

    for i in range(0,3):
        # print("query", i)
        queryFaceIds[i] = getFaceId(querys[i])

    # print(queryFaceIds)

    for i in range(0, len(datas)):
        # print("data", i)
        dataFaceIds.append(getFaceId(datas[i]))
        idToUrl[dataFaceIds[i]] = datas[i]

    # print(dataFaceIds)

    list = {}

    for i in range(0,3):
        list[i] = getConfidenceList(queryFaceIds[i], dataFaceIds)

    result = {}
    for val in dataFaceIds:
        # result[val] = minScore(list, val)
        result[val] = aveScore(list, val)

    urls = {}
    # 降順にprint
    for key, val in sorted(result.items(), key = lambda x:-x[1]):
        # print(key, val)
        # print('    url:', idToUrl[key])
        urls[idToUrl[key]] = val

    return urls



def search_category_fool(faceType):
    querys = {  'satou':[
                    'http://netacube.com/wp-content/uploads/2016/10/ryo.jpg',
                    'https://idobatakaigi0510.com/wp-content/uploads/2016/02/3e0d2eed.jpg',
                    'https://news.walkerplus.com/article/89761/504110_615.jpg',
                ],
                'sio':[
                    'http://tristone.co.jp/actors/img/sakaguchi350.jpg',
                    'https://i0.wp.com/free-style-info.com/wp-content/uploads/2017/05/smallbigman_okada005-20170528.jpg?resize=300%2C300&ssl=1',
                    'https://images-na.ssl-images-amazon.com/images/I/71pnv7I3O7L.jpg',
                ],
                'syouyu':[
                    'http://foreverfllow.com/wp-content/uploads/2015/01/qql.jpg',
                    'http://geinou11.com/wp-content/uploads/2017/06/osamu00-272x300.jpg',
                    'http://yorozu-do.com/wp-content/uploads/2016/07/b5dd3950556d5db78568c73e642a0b63.jpg',
                ],
                'sousu':[
                    'http://abehiroshi.la.coocan.jp/abe-top2-4.jpg',
                    'https://pbs.twimg.com/media/CdWDqoQUsAA_0gF.jpg',
                    'https://pbs.twimg.com/profile_images/561077710856806400/tdl6wF0h.jpeg',
                ],
            }

    datas = [
                'http://www.takumi-jun.com/contents/upload-images/201458221929.jpg',
                'http://www.isetan-photo.co.jp/sp/shomei/images/recruit_slide04.jpg',
                'http://asakusa-link.com/wp-content/uploads/2016/03/74e3b8ee00cb35feef211ebdc8c76796_s.jpg',
                'http://img01.osakazine.net/usr/s/t/u/studiolib/bst_24135dd.jpg',
                'https://ranking.xgoo.jp/tool/images/column/2016/06/0610_11re.jpg',
                'https://i2.wp.com/nekotopi.com/wp-content/uploads/2014/10/cm-abe.jpg',
                'https://contents.oricon.co.jp/photo/img/0/259/detail/img660/0_84691200_1340881653.jpg',

                'https://pbs.twimg.com/media/CmrqLy_VMAITSo-.jpg',
                'http://stat.news.ameba.jp/news_images/20151116/07/70/VD/j/o03820434ayanogo.jpg',
                'http://image.space.rakuten.co.jp/d/strg/ctrl/9/4fa00c525815bfc2044ad03a63de4a8cfc57d5a9.66.2.9.2.jpeg',
                'http://i2.w.yun.hjfile.cn/slide/201312/21983267836.jpg',

                'http://eiga.k-img.com/images/person/83877/300x.jpg',
            ]

    queryFaceIds = {}
    dataFaceIds = []
    idToUrl = {}

    for i in range(0,3):
        # print("query", i)
        queryFaceIds[i] = getFaceId(querys[faceType][i])

    # print(queryFaceIds)

    for i in range(0, len(datas)):
        # print("data", i)
        dataFaceIds.append(getFaceId(datas[i]))
        idToUrl[dataFaceIds[i]] = datas[i]

    # print(dataFaceIds)

    list = {}

    for i in range(0,3):
        list[i] = getConfidenceList(queryFaceIds[i], dataFaceIds)

    result = {}
    for val in dataFaceIds:
        # result[val] = minScore(list, val)
        result[val] = aveScore(list, val)

    urls = {}
    # 降順にprint
    for key, val in sorted(result.items(), key = lambda x:-x[1]):
        # print(key, val)
        # print('    url:', idToUrl[key])
        urls[idToUrl[key]] = val

    return urls


def search_category(faceType):
    datas = [
                'http://www.takumi-jun.com/contents/upload-images/201458221929.jpg',
                'http://www.isetan-photo.co.jp/sp/shomei/images/recruit_slide04.jpg',
                'http://asakusa-link.com/wp-content/uploads/2016/03/74e3b8ee00cb35feef211ebdc8c76796_s.jpg',
                'http://img01.osakazine.net/usr/s/t/u/studiolib/bst_24135dd.jpg',
                'https://ranking.xgoo.jp/tool/images/column/2016/06/0610_11re.jpg',
                'https://i2.wp.com/nekotopi.com/wp-content/uploads/2014/10/cm-abe.jpg',
                'https://contents.oricon.co.jp/photo/img/0/259/detail/img660/0_84691200_1340881653.jpg',

                'https://pbs.twimg.com/media/CmrqLy_VMAITSo-.jpg',
                'http://stat.news.ameba.jp/news_images/20151116/07/70/VD/j/o03820434ayanogo.jpg',
                'http://image.space.rakuten.co.jp/d/strg/ctrl/9/4fa00c525815bfc2044ad03a63de4a8cfc57d5a9.66.2.9.2.jpeg',
                'http://i2.w.yun.hjfile.cn/slide/201312/21983267836.jpg',

                'http://eiga.k-img.com/images/person/83877/300x.jpg',
            ]

    queryFaceIds = {}
    dataFaceIds = []
    idToUrl = {}

    result = {}


    for i in range(0, len(datas)):
        # print("data", i)
        faceId = getFaceId(datas[i])
        dataFaceIds.append(faceId)
        result[datas[i]] = getCvScore(datas[i], faceType)
        # idToUrl[dataFaceIds[i]] = datas[i]

    url = {}

    for key, val in sorted(result.items(), key = lambda x:-x[1]):
        url[key] = val

    return url


def getFaceId(url):
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'c47c7f33d73a4d1b8a8dff1f679e6b2f',
    }

    body = {
        'url':url
    }

    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        # print(data[0]['faceId'])
        conn.close()
        return data[0]['faceId']
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# faceId: query, faceIds: data
# return: list{'faceId' => 'confidience'}
def getConfidenceList(faceId, faceIds):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'c47c7f33d73a4d1b8a8dff1f679e6b2f',
    }

    body = {
        'faceId':faceId,
        'faceIds':faceIds,
        "mode": "matchFace"
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/findsimilars?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        list = {}
        for tmp in data:
            list[tmp['faceId']] = tmp['confidence']
        return list
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def getCvScore(dataUrl, faceType):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Prediction-key': '6eba1a71f69840b384f05781751ce2fc',
    }

    params = urllib.parse.urlencode({
        'iterationId': 'e03f94da-a05e-4fdf-b540-8a02772e9875',
    })

    body = {
        'url':dataUrl
    }

    try:
        conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        # f = open("violin_a.jpg", "rb", buffering=0)
        conn.request("POST", "/customvision/v1.0/Prediction/2f7c6536-5766-4aa5-800d-556f895167d9/url?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        for tmp in data['Predictions']:
            if(tmp['Tag'] == faceType):
                return tmp['Probability']
    except Exception as e:
        # print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print(e)


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


# ******************************************************


# Import a module / component using its blueprint handler variable (mod_auth)
from app.controller.users import mod_users

# Register blueprint(s)
app.register_blueprint(mod_users)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

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
    urls = list(map(lambda image: image["contentUrl"], data["value"]))[:3] # 上位3つだけ使う
    # print(urls)
    conn.close()
    return urls

# Import a module / component using its blueprint handler variable (mod_auth)
from app.controller.users import mod_users

# Register blueprint(s)
app.register_blueprint(mod_users)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# Configure the image uploading via Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

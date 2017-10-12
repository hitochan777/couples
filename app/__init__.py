# Import flask and template operators
from flask import Flask, render_template, request, redirect

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/search", methods=['GET'])
def search():
    personName = request.args.get('search-text')
    if personName is None or len(personName) == 0:
        return redirect("/", code=302)

    return render_template('search_result.html')


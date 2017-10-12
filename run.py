from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    print(name)
    return render_template('index.html', name=name)

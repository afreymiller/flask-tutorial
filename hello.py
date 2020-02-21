from flask import Flask

app = Flask(__name__)

# env FLASK_APP=hello.py flask run

@app.route("/")
def hello():
    return "Hello, World!"
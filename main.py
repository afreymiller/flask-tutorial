from flask import Flask

app = Flask(__name__)

# Docs: https://flask.palletsprojects.com/en/1.1.x/

# env FLASK_APP=main.py flask run

@app.route("/")
def main():
    return "Hello, World!"
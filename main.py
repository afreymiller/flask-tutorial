from flask import Flask, jsonify
from markupsafe import escape
import requests
from review_field_utils import populate_review_fields, construct_url, parse_response_for_reviews

app = Flask(__name__)

# Docs: https://flask.palletsprojects.com/en/1.1.x/

# env FLASK_APP=main.py flask run

@app.route('/')
def index():
    return 'Index Page'

def execute_request(url):
    return requests.get(url)

@app.route('/reviews/<lender>/<int:number>')
def get_reviews(lender, number):
    url = construct_url(lender, number)
    response = requests.get(url)
    objects = parse_response_for_reviews(response)
    
    return jsonify(reviews=objects)
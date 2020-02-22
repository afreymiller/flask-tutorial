from flask import Flask, jsonify
from markupsafe import escape
import requests
from review_field_utils import populate_review_fields, construct_url, parse_response_for_reviews

app = Flask(__name__)

# Docs: https://flask.palletsprojects.com/en/1.1.x/

# env FLASK_APP=main.py flask run

# http://127.0.0.1:5000/reviews/upstart-network-inc/54350158

@app.route('/')
def index():
    return 'Index Page'

def execute_request(url):
    return requests.get(url)

@app.route('/reviews/<lender>/<int:review_id>')
def get_reviews(lender, review_id):
    try: 
        url = construct_url(lender, review_id)
        response = requests.get(url)

        objects = parse_response_for_reviews(response)
    
        return jsonify(reviews=objects)
    except ValueError:
        return "Input for review_id should be an integer"
    except AttributeError:
        return "Input for lender should be a non-null string"
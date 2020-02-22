from flask import Flask, jsonify
from markupsafe import escape
import requests
from review_field_utils import populate_review_fields, construct_url, parse_reviews, get_reviews_from_response

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
        url1 = construct_url(lender, review_id, 5, 1)
        responses = []
        response1 = requests.get(url1)

        url2 = construct_url(lender, review_id, 5, 2)
        response2 = requests.get(url2)

        url3 = construct_url(lender, review_id, 5, 3)
        response3 = requests.get(url3)

        responses.append(response1)
        responses.append(response2)
        responses.append(response3)

        #if (response.status_code < 200 or response.status_code > 299):
        #    return "Did not get successful response: " + str(response.status_code) 
        objects_aggregated = []
        for response in responses:
            reviews = get_reviews_from_response(response)
            objects = parse_reviews(reviews)
            objects_aggregated.append(objects)
        return jsonify(reviews=objects_aggregated)
    except ValueError:
        return "Input for review_id should be a non-negative integer"
    except AttributeError:
        return "Input for lender should be a non-null string"
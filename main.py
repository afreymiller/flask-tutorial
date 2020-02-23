from flask import Flask, jsonify
from markupsafe import escape
import requests
from review_field_utils import populate_review_fields, construct_url_prefix, parse_reviews, get_reviews_from_response
import threading 
import concurrent.futures

app = Flask(__name__)

# Docs: https://flask.palletsprojects.com/en/1.1.x/

# env FLASK_APP=main.py flask run

# http://127.0.0.1:5000/reviews/upstart-network-inc/54350158

@app.route('/')
def index():
    return 'Index Page'

def execute_request(url):
    return requests.get(url)

def get_response(lender, review_id, star_rating):

    # helpful: https://www.hackerearth.com/practice/python/functional-programming/higher-order-functions-and-decorators/tutorial/

    url_prefix = construct_url_prefix(lender, review_id, star_rating)

    def execute(page_index):
        url = url_prefix + '&pid=' + str(page_index)
        print(url)
        return execute_request(url)
    
    return execute

@app.route('/reviews/<lender>/<int:review_id>')
def get_reviews(lender, review_id):
    try: 
        #page_index = 1
        #url = construct_url(lender, review_id, 5, page_index)
        #response = requests.get(url)
        responses = []
        closure = get_response(lender, review_id, 5)

        #while (response.status_code >= 200 and response.status_code <= 299):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.map(closure, range(200))
            responses = [x for x in future]

        # while (page_index < 15):
        #     responses.append(response)
        #     page_index += 1
        #     url = construct_url(lender, review_id, 4, page_index)
        #     print(page_index)
        #     response = requests.get(url)

        print(len(responses))
        print(responses)

        #if (response.status_code < 200 or response.status_code > 299):
        #    return "Did not get successful response: " + str(response.status_code) 

        objects_aggregated = []
        for response in responses:
            reviews = get_reviews_from_response(response)
            objects = parse_reviews(reviews)
            objects_aggregated.append(objects)
        print(len(objects_aggregated))
        return jsonify(reviews=objects_aggregated)
    except ValueError:
        return "Input for review_id should be a non-negative integer"
    except AttributeError:
        return "Input for lender should be a non-null string"
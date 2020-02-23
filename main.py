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
        response = execute_request(url)
        reviews = get_reviews_from_response(response)
        objects = parse_reviews(reviews)
        return objects
    
    return execute

@app.route('/reviews/<lender>/<int:review_id>')
def get_reviews(lender, review_id):
    try: 
        #page_index = 1
        #url = construct_url(lender, review_id, 5, page_index)
        #response = requests.get(url)
        objects_agg_5 = []
        objects_agg_4 = []
        objects_agg_3 = []
        objects_agg_2 = []
        objects_agg_1 = []
        closure_5 = get_response(lender, review_id, 5)
        closure_4 = get_response(lender, review_id, 4)
        closure_3 = get_response(lender, review_id, 3)
        closure_2 = get_response(lender, review_id, 2)
        closure_1 = get_response(lender, review_id, 1)

        #while (response.status_code >= 200 and response.status_code <= 299):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_5 = executor.map(closure_5, range(200))
            future_4 = executor.map(closure_4, range(10))
            future_3 = executor.map(closure_3, range(10))
            future_2 = executor.map(closure_2, range(10))
            future_1 = executor.map(closure_1, range(10))
            objects_agg_5 = [x for sublist in future_5 for x in sublist]
            objects_agg_4 = [x for sublist in future_4 for x in sublist]
            objects_agg_3 = [x for sublist in future_3 for x in sublist]
            objects_agg_2 = [x for sublist in future_2 for x in sublist]
            objects_agg_1 = [x for sublist in future_1 for x in sublist]

        objects_agg_5.append(objects_agg_4)
        objects_agg_5.append(objects_agg_3)
        objects_agg_5.append(objects_agg_2)
        objects_agg_5.append(objects_agg_1)

        #if (response.status_code < 200 or response.status_code > 299):
        #    return "Did not get successful response: " + str(response.status_code) 

        return jsonify(reviews=objects_agg_5)
    except ValueError:
        return "Input for review_id should be a non-negative integer"
    except AttributeError:
        return "Input for lender should be a non-null string"
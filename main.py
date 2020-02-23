from flask import Flask, jsonify
from markupsafe import escape
import requests
from review_field_utils import populate_review_fields, construct_url_prefix, parse_reviews, get_reviews_from_response
import threading 
import concurrent.futures
import bs4
import re
import math
from bs4 import BeautifulSoup, Tag

app = Flask(__name__)

# Docs: https://flask.palletsprojects.com/en/1.1.x/

# env FLASK_APP=main.py flask run

# http://127.0.0.1:5000/reviews/upstart-network-inc/54350158

# https://www.lendingtree.com/reviews/personal/upstart-network-inc/54350158

# https://www.lendingtree.com/reviews/personal/cashnetusa/81638970

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
        objects = parse_reviews(reviews, star_rating)
        return objects
    
    return execute

@app.route('/reviews/<lender>/<int:review_id>')
def get_reviews(lender, review_id):
    try: 
        objects_ag = []
        flattened = []

        url = construct_url_prefix(lender, review_id, 5)
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')   
        star_count = soup.select(".review-count-text")

        # Maybe use ::-1 here

        star_frequencies = []
            
        # make this more readable
        for frequency in star_count:
            freq_as_int = int(re.sub(r'[\(\)]', '', frequency.contents[0]))
            page_count = (math.ceil(freq_as_int/10)) + 1
            star_frequencies.append(page_count)

        in_order = star_frequencies[::-1]

        closures = [get_response(lender, review_id, x) for x in range(1, 6)]

        # https://gist.github.com/mangecoeur/9540178

        futures = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for index, closure in enumerate(closures):
                future = executor.map(closure, range(in_order[index]))
                futures.append(future)

        # Should the following lines be part of the thread pool executor?
        objects_ag = [x for sublist in futures for x in sublist]
        flattened = [x for sublist in objects_ag for x in sublist]

        #if (response.status_code < 200 or response.status_code > 299):
        #    return "Did not get successful response: " + str(response.status_code) 

        print(len(flattened))

        return jsonify(reviews=flattened)
    except ValueError:
        return "Input for review_id should be a non-negative integer"
    except AttributeError:
        return "Input for lender should be a non-null string"
from flask import Flask, jsonify
from markupsafe import escape
import requests
from review_field_utils import populate_review_fields, get_star_frequencies, execute_thread_pool
from review_field_utils import construct_url_prefix, parse_reviews, get_flattened_reviews_from_futures
from review_field_utils import get_reviews_from_response
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

# http://127.0.0.1:5000/reviews/cashnetusa/81638970

# https://www.lendingtree.com/reviews/personal/upstart-network-inc/54350158

# https://www.lendingtree.com/reviews/personal/cashnetusa/81638970

@app.route('/')
def index():
    return 'Index Page'

def execute_request(url):
    return requests.get(url)

def get_response_closure(lender, review_id, page_limit_for_star, star_rating):

    # helpful: https://www.hackerearth.com/practice/python/functional-programming/higher-order-functions-and-decorators/tutorial/

    url_prefix = construct_url_prefix(lender, review_id, star_rating)

    def execute(page_index):
        url = ""

        if (page_limit_for_star <= 2):
            url = url_prefix
        else:
            url = url_prefix + '&pid=' + str(page_index)
        
        response = execute_request(url)

        objects = []

        if response.status_code >= 200 or respose.status_code <= 299:
            reviews = get_reviews_from_response(response)
            objects = parse_reviews(reviews, star_rating)

        return objects
    
    return execute

def reviews_are_equal(review_1, review_2):
    dates_equal = review_1["date"] == review_2["date"]
    titles_equal = review_1["title"] == review_2["title"]
    names_equal = review_1["name"] == review_2["name"]
    stars_equal = review_1["stars"] == review_2["stars"]
    values_equal = review_1["value"] == review_2["value"]

    return dates_equal and titles_equal and names_equal and stars_equal and values_equal

@app.route('/reviews/<lender>/<int:review_id>')
def get_reviews(lender, review_id):
    try: 
        page_counts_per_star = get_star_frequencies(lender, review_id)

        closures = [get_response_closure(lender, review_id, page_counts_per_star[x], x+1) for x in range(5)]

        # https://gist.github.com/mangecoeur/9540178

        futures = execute_thread_pool(closures, page_counts_per_star)

        flattened = get_flattened_reviews_from_futures(futures)

        new_flattened = []

        for review in flattened:
            filtered_objs = [item for item in new_flattened if reviews_are_equal(item, review)]
            if (len(filtered_objs) == 0):
                new_flattened.append(review)

        print(len(new_flattened))

        return jsonify(reviews=new_flattened)
    except ValueError:
        return "Input for review_id should be a non-negative integer"
    except AttributeError:
        return "Input for lender should be a non-null string"
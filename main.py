from flask import Flask, jsonify
from markupsafe import escape
import requests
# Importing a lot from reviews_utils, don't want to use wildcard (*) imports
from reviews_utils import populate_review_fields, get_page_limits, execute_thread_pool
from reviews_utils import construct_url_prefix, parse_reviews, get_flattened_reviews_from_futures
from reviews_utils import reviews_are_equal, execute_request, get_response_closure
import threading 
import concurrent.futures
import bs4
import re
import math
from bs4 import BeautifulSoup, Tag

app = Flask(__name__)

# Run using command `env FLASK_APP=main.py flask run`

# Example request: http://127.0.0.1:5000/reviews/upstart-network-inc/54350158

@app.route('/')
def index():
    return 'Index Page'

@app.route('/reviews/<lender>/<int:review_id>')
def get_reviews(lender, review_id):
    try: 
       
        page_counts_per_star = get_page_limits(lender, review_id)

        closures = [get_response_closure(lender, review_id, page_counts_per_star[x], x+1) for x in range(5)]

        futures = execute_thread_pool(closures, page_counts_per_star)

        flattened_reviews = get_flattened_reviews_from_futures(futures)

        duplicates_removed = []

        for review in flattened_reviews:
            filtered_objs = [item for item in duplicates_removed if reviews_are_equal(item, review)]
            if (len(filtered_objs) == 0):
                duplicates_removed.append(review)

        return jsonify(reviews_count=len(duplicates_removed),reviews=duplicates_removed)
    except ValueError:
        return "Input for review_id should be a non-negative integer"
    except AttributeError:
        return "Input for lender should be a non-null string"
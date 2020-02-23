from flask import Flask, jsonify
from markupsafe import escape
import requests
from reviews_utils import populate_review_fields, get_star_frequencies, execute_thread_pool
from reviews_utils import construct_url_prefix, parse_reviews, get_flattened_reviews_from_futures
from reviews_utils import reviews_are_equal, execute_request, get_response_closure
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

@app.route('/reviews/<lender>/<int:review_id>')
def get_reviews(lender, review_id):
    try: 
       
        page_counts_per_star = get_star_frequencies(lender, review_id)

        closures = [get_response_closure(lender, review_id, page_counts_per_star[x], x+1) for x in range(5)]

        # https://gist.github.com/mangecoeur/9540178

        futures = execute_thread_pool(closures, page_counts_per_star)

        flattened_reviews = get_flattened_reviews_from_futures(futures)

        duplicates_removed = []

        for review in flattened_reviews:
            filtered_objs = [item for item in duplicates_removed if reviews_are_equal(item, review)]
            if (len(filtered_objs) == 0):
                duplicates_removed.append(review)

        #print(len(duplicates_removed))

        return jsonify(reviews_count=len(duplicates_removed),reviews=duplicates_removed)
    except ValueError:
        return "Input for review_id should be a non-negative integer"
    except AttributeError:
        return "Input for lender should be a non-null string"
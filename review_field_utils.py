import bs4
from bs4 import BeautifulSoup, Tag
import requests
import re
import math
import threading 
import concurrent.futures

# Added positive unit tests, will add some more negative ones
def populate_review_fields(review, star_rating):
    # These should ideally come from either a database or parameter store, 
    # but for the purposes of this exercise I'll leave them here for now.
    field_dependencies = [{
            "selector": ".reviewText",
            "key": "value"
        }, {
            "selector": ".reviewTitle",
            "key": "title"
        }, {
            "selector": ".consumerName",
            "key": "name"
        }, {
            "selector": ".consumerReviewDate",
            "key": "date"
        }
    ]

    obj = {}

    for field in field_dependencies: 
        element = review.select(field['selector'])
        value = element[0]

        # Checking for type of Tag due to one edge case related to <br/> tags found
        text = [x for x in value.contents if type(x) != Tag]

        obj[field['key']] = text[0].strip()

    obj['stars'] = star_rating

    return obj

# Probably won't get to unit testing this one before the deadline
def execute_thread_pool(closures, page_counts_per_star):
    futures = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for index, closure in enumerate(closures):
            future = executor.map(closure, range(page_counts_per_star[index]))
            futures.append(future)

    return futures

# Probably won't get to unit testing this one because I'm not sure how to
# create a future without just calling executor thread map
def get_flattened_reviews_from_futures(futures):
    objects_ag = [x for sublist in futures for x in sublist]

    flattened_reviews = [x for sublist in objects_ag for x in sublist]

    return flattened_reviews

# Unit testing complete
def construct_url_prefix(lender, review_id, star_rating):
    try:
        id_as_int = int(review_id)

        # From observations, pretty sure flask's routing already throws 
        # an error for negative values but just in case...
        if (id_as_int < 0):
            raise ValueError("review_id should be a non-negative integer.")

        if (len(lender) <= 0):
            raise RuntimeError("Lender must be non-null")

        lender = lender.strip()

        URL_PREFIX = "https://www.lendingtree.com/reviews/personal/"
        url = URL_PREFIX + lender
        url += "/"
        url += str(review_id)
        url += f'?OverallRating={star_rating}' #&pid={page}'
        return url

    except ValueError:
        raise ValueError("review_id should be a non-negative integer.")
    except TypeError:
        raise TypeError("Input for lender should be a string")
    except RuntimeError:
        raise RuntimeError("Lender must be non-null")

# not unit testing this one unless I have extra time at the end
def get_reviews_from_response(response):
    soup = BeautifulSoup(response.content, 'html.parser')   
    reviews = soup.select(".reviewDetail")
    return reviews

def get_star_frequencies(lender, review_id):
    url = construct_url_prefix(lender, review_id, 5)
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')   
    star_count = soup.select(".review-count-text")

    star_frequencies = []
            
    # make this more readable
    for frequency in star_count:
        freq_as_int = int(re.sub(r'[\(\)]', '', frequency.contents[0]))
        page_count = (math.ceil(freq_as_int/10)) + 1
        star_frequencies.append(page_count)

    in_order = star_frequencies[::-1]

    return in_order

def parse_reviews(reviews, star_rating):

    objects = []

    for review in reviews:
        obj = populate_review_fields(review, star_rating)
        objects.append(obj)

    return objects
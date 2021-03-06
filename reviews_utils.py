import bs4
from bs4 import BeautifulSoup, Tag
import requests
import re
import math
import threading 
import concurrent.futures


# Added positive unit tests, will add some more negative ones
def populate_review_fields(review, star_rating):
    """ 
    Given a review tag and star_rating, populates a dictionary
    with appropriate fields.
  
    Parameters: 
    review (Tag): html div tag of review containing all info to parse.
    star_rating (int): 1-5
  
    Returns: 
    Dictionary of appropriate review fields.
    """

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
            "key": "author"
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

# Added positive and negative unit tests
def reviews_are_equal(review_1, review_2):
    """ 
    Given two review objects, returns true if they are equal, false otherwise.
  
    Parameters: 
    review_1: review object
    review_2: review object
  
    Returns: 
    Boolean, True if they're, equal. False if not.
    """
    fields = ["date", "title", "author", "stars", "value"]

    are_equal = True

    for field in fields:
        are_equal &= review_1[field] == review_2[field]

    return are_equal

# Unit testing complete
def construct_url_prefix(lender, review_id, star_rating):
    """ 
    Given lender, id, and star rating, returns URL for GET.
  
    Parameters: 
    lender: String
    review_id: String/int
    star_rating: int
  
    Returns: 
    URL string.
    """
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

# Add unit tests
def get_page_limits(lender, review_id):
    '''
    Given lender and review_id, returns the 
    '''
    url = construct_url_prefix(lender, review_id, 5)
    response = execute_request(url)

    star_counts = get_tags_of_selector_from_response(response, ".review-count-text")

    star_frequencies = []
            
    # make this more readable
    for frequency in star_counts:
        freq_as_int = int(re.sub(r'[\(\)]', '', frequency.contents[0]))
        page_count = (math.ceil(freq_as_int/10)) + 1
        star_frequencies.append(page_count)

    in_order = star_frequencies[::-1]

    return in_order

def parse_reviews(reviews, star_rating):
    '''
    Get list of all populated review objects given review tags and star rating.
    '''
    objects = []

    for review in reviews:
        obj = populate_review_fields(review, star_rating)
        objects.append(obj)

    return objects

# Not writing unit tests for this one
def get_tags_of_selector_from_response(response, selector):
    '''
    Given response and CSS selector, parse the response contents and return
    tags.
    '''
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.select(selector)

# Probably won't get to unit testing this one because I'm not sure how to
# create a future without just calling executor thread map
def get_flattened_reviews_from_futures(futures):
    '''
    Flatten futures into format that is returned in JSON.
    '''
    objects_ag = [x for sublist in futures for x in sublist]

    flattened_reviews = [x for sublist in objects_ag for x in sublist]

    return flattened_reviews

# Probably won't get to unit testing this one before the deadline
def execute_thread_pool(closures, page_counts_per_star):
    futures = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for index, closure in enumerate(closures):
            future = executor.map(closure, range(page_counts_per_star[index]))
            futures.append(future)

    return futures

# Not writing unit tests for this one
def execute_request(url):
    return requests.get(url)

# Not writing unit tests for this one
def get_response_closure(lender, review_id, page_limit_for_star, star_rating):

    '''
    Closure for allowing one to call the execute function with the parent arguments
    in the context of the thread map executor.
    '''

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
            reviews = get_tags_of_selector_from_response(response, '.reviewDetail')
            objects = parse_reviews(reviews, star_rating)

        return objects
    
    return execute
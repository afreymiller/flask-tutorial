import bs4
from bs4 import BeautifulSoup

def populate_review_fields(review):
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
        obj[field['key']] = value.contents[0].strip()

    return obj

def construct_url(lender, review_id):
    try:
        id_as_int = int(review_id)
        lender = lender.strip()

        URL_PREFIX = "https://www.lendingtree.com/reviews/personal/"
        full_url = URL_PREFIX + lender
        full_url += "/"
        full_url += str(review_id)
        full_url += "?OverallRating=1&pid=1"
        return full_url
        
    except ValueError:
        raise ValueError("Input for review_id should be an integer")
    except AttributeError:
        raise AttributeError("Input for lender should be a non-null string")

def parse_response_for_reviews(response):
    soup = BeautifulSoup(response.content, 'html.parser')   
    reviews = soup.select(".reviewDetail")

    objects = []

    for review in reviews:
        obj = populate_review_fields(review)
        objects.append(obj)

    return objects
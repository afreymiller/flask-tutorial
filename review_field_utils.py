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

def construct_url(lender, number):
    URL_PREFIX = "https://www.lendingtree.com/reviews/personal/"
    URL_PREFIX += lender
    URL_PREFIX += "/"
    URL_PREFIX += str(number)
    URL_PREFIX += "?OverallRating=1&pid=1"
    return URL_PREFIX

def parse_response_for_reviews(response):
    soup = BeautifulSoup(response.content, 'html.parser')   
    reviews = soup.select(".reviewDetail")

    objects = []

    for review in reviews:
        obj = populate_review_fields(review)
        objects.append(obj)

    return objects
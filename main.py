from flask import Flask, jsonify
from markupsafe import escape
import requests
import bs4
from bs4 import BeautifulSoup

app = Flask(__name__)

# Docs: https://flask.palletsprojects.com/en/1.1.x/

# env FLASK_APP=main.py flask run

@app.route('/')
def index():
    return 'Index Page'

def construct_url(lender, number):
    URL_PREFIX = "https://www.lendingtree.com/reviews/personal/"
    URL_PREFIX += lender
    URL_PREFIX += "/"
    URL_PREFIX += str(number)
    URL_PREFIX += "?OverallRating=1&pid=1"
    return URL_PREFIX

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

def get_reviews_object(lender, number):
    url = construct_url(lender, number)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')   

    reviews = soup.select(".reviewDetail")

    objects = []

    for review in reviews:
        obj = populate_review_fields(review)
        objects.append(obj)

    return objects

@app.route('/reviews/<lender>/<int:number>')
def get_reviews(lender, number):
    
    objects = get_reviews_object(lender, number)
    
    return jsonify(reviews=objects)
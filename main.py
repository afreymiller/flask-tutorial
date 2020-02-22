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
    review_text = review.select(".reviewText")     
    review_title = review.select(".reviewTitle") 
    reviewer_name = review.select(".consumerName")
    review_date = review.select(".consumerReviewDate")

    obj = {}
  
    value = review_text[0]  
    title = review_title[0]     
    name = reviewer_name[0]
    date = review_date[0]

    obj['value'] = value.contents[0].strip()
    obj['title'] = title.contents[0].strip()
    obj['name'] = name.contents[0].strip()
    obj['date'] = date.contents[0].strip()

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

@app.route('/dummy/<username>/<int:number>')
def get_nested(username, number):
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
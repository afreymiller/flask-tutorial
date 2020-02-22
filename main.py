from flask import Flask
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

@app.route('/review')
def get_reviews():
    url = "https://www.lendingtree.com/reviews/personal/cashnetusa/81638970?OverallRating=4&pid=3"
    response = requests.get(url)                                                                     
    soup = BeautifulSoup(response.content, 'html.parser')   

    review_text = soup.select(".reviewText")     
    review_title = soup.select(".reviewTitle") 
  
    value = review_text[0]   
    print(value) 

    title = review_title[0]                                                                                                              

    return str(value) + str(title)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
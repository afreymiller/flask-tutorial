## Lender Review Parsing Exercise

**Purpose:** Create a lightweight API to scrape lendingtree.com for relevant review data from different lenders.

**Tools used:** Python, Flask, bs4

### Usage

To run locally, follow these steps:

1. Ensure most recent version of Flask is downloaded (if not, download using pip via the command `pip3 install Flask`. You might have to put a --user flag at the end of that command)

2. Clone this repo locally.

3. In the root directory, run `env FLASK_APP=main.py flask run`.

4. Open your browser and enter a URL of the form: `http://127.0.0.1:5000/reviews/<LENDER_NAME>/<ID>`. 
Some common variants that I used during manual checks included http://127.0.0.1:5000/reviews/cashnetusa/81638970
and http://127.0.0.1:5000/reviews/upstart-network-inc/54350158. 

5. After hitting enter, in a few seconds you'll see JSON returned to the screen that contains the reviews for
that lender and ID with the following format:

{
  "reviews": list of all reviews,
  "reviews_count": number of reviews in response
}

Each review is a dictionary with "title", "stars", "author", "value", "date" keys, e.g.

{
  "author": "John Doe",
  "title": "Great job!",
  "value": "Good service blah blah blah",
  "date": "Reviewed in September 2019",
  "stars" 5
}

6. Unit tests can be run with the command `python3 unit_tests.py`.


## Notes

The routing can be found in main.py, a module containing most of the functionality can be found in reviews_utils.py,
and unit tests can be found in unit_tests.py. For the unit tests, I'm aware that a couple of them are not "true"
unit tests because they don't run offline and they don't mock dependencies (most notably BeautifulSoup), but
I believe that given the time constraints this is agreeable.

I used a thread pool executor to parallelize the tasks of making all the GET requests to lendingtree.com and some of
the subsequent parsing which helped save a good chunk of time vs. doing it iteratively.

While I'm happy that my implementation has aggregated most of the reviews for a given lender name and id, I
did notice some edge cases that I was not able to resolve. When I go to https://www.lendingtree.com/reviews/personal/cashnetusa/81638970, there are 1732 reviews, but my equivalent request returns 1724, with there being four 3 and 4-star reviews missing. I was also not able to get as much unit testing and exception handling done as I would have preferred. Any feedback is welcome and can be sent to afreymiller10@gmail.com.
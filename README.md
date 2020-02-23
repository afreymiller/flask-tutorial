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



## Notes

While I'm happy that my implementation has aggregated most of the reviews for a given lender name and id 
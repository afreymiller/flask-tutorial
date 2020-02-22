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

def construct_url(lender, review_id, star_rating, page):
    try:
        id_as_int = int(review_id)

        if (id_as_int < 0):
            raise ValueError("review_id should be a non-negative integer.")

        if (len(lender) <= 0):
            raise RuntimeError("Lender must be non-null")

        lender = lender.strip()

        URL_PREFIX = "https://www.lendingtree.com/reviews/personal/"
        full_url = URL_PREFIX + lender
        full_url += "/"
        full_url += str(review_id)
        full_url += f'?OverallRating={star_rating}&pid={page}'
        return full_url

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

def parse_reviews(reviews):

    objects = []

    for review in reviews:
        obj = populate_review_fields(review)
        objects.append(obj)

    return objects

def exception_parent(string):
    try:
        exception_child(string)
    except RuntimeError:
        raise RuntimeError("nullity")
    except:
        raise Exception("generic exception")

def exception_child(string):
    try: 
        if (len(string) <= 0):
            raise RuntimeError("Null string")
        else:
            return string
    except RuntimeError:
        raise RuntimeError("the string was null")
    except ValueError:
        raise ValueError("this was the one")
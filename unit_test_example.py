import unittest
from reviews_utils import populate_review_fields, construct_url_prefix, parse_reviews, reviews_are_equal
import bs4
from bs4 import BeautifulSoup

# https://docs.python.org/3/library/unittest.html

class TestStringMethods(unittest.TestCase):

    def test_construct_url_prefix_1(self):
      expected_url_1 = "https://www.lendingtree.com/reviews/personal/cashnetusa/81638970?OverallRating=1"
      self.assertEqual(construct_url_prefix('cashnetusa', '81638970', 1), expected_url_1)

    def test_construct_url_prefix_2(self):      
      with self.assertRaises(ValueError) as context:
            construct_url_prefix('cashnetusa', 'abc', 1)

      self.assertTrue('review_id should be a non-negative integer.' in str(context.exception))
      
    def test_construct_url_prefix_3(self):
      
      with self.assertRaises(TypeError) as context:
            construct_url_prefix(3, '1234123', 1)

      self.assertTrue('Input for lender should be a string' in str(context.exception))

    def test_construct_url_prefix_4(self):      
      with self.assertRaises(RuntimeError) as context:
            construct_url_prefix("", '1234123', 1)

      self.assertTrue('Lender must be non-null' in str(context.exception))

    def test_construct_url_prefix_5(self):
      
      with self.assertRaises(ValueError) as context:
            construct_url_prefix('cashnetusa', '-5', 1)

      self.assertTrue('review_id should be a non-negative integer.' in str(context.exception))

    def test_populate_review_fields_1(self):
      review1 = '''
        <div class="col-lg-9 col-sm-8 col-xs-12 reviewDetail">
        <p class="reviewTitle">Excellent Customer Service</p>
        <p class="reviewText">Kara at Wyndham Capitol is the Queen of Refi. If your looking for great service and a easy hassle free refi or new home loan look no further!</p>
        <div aria-hidden="true" class="hideText">
        <p class="consumerName">Richard's                                                                        <span>from BEL AIR, MD</span></p>
        <p class="consumerReviewDate">Reviewed in February 2020</p>
        </div>
        <div class="helpfull-count desktop-view">
        <div class="helpfull-section">
        <input class="reviewId" name="reviewId" type="hidden" value="5e4c78ae13c6370001bb56f5"/>
        <div class="flagged-review">
        <button aria-label="Mark this review as flagged" class="flag" id="flag-5e4c78ae13c6370001bb56f5">
        <div class="flag-content">
        <img alt="" src="https://www.lendingtree.com/content/themes/lt-wp-www-theme/dist/images/lender-review/review-flag-desktop.png"/>
        <span class="flag-text">Flag review</span>
        </div>
        </button>
        </div>
        </div>
        </div>
        </div>
      '''

      review_1_as_soup = BeautifulSoup(review1, 'html.parser')

      output_1 = populate_review_fields(review_1_as_soup, 5)

      self.assertTrue('value' in output_1)
      self.assertTrue('name' in output_1)
      self.assertTrue('title' in output_1)
      self.assertTrue('date' in output_1)
      self.assertTrue('stars' in output_1)
      self.assertEqual(output_1['date'], "Reviewed in February 2020")
      self.assertEqual(output_1['name'], "Richard's")
      self.assertEqual(output_1['title'], "Excellent Customer Service")
      self.assertEqual(output_1['value'], "Kara at Wyndham Capitol is the Queen of Refi. If your looking for great service and a easy hassle free refi or new home loan look no further!")
      self.assertEqual(output_1['stars'], 5)
    
    def test_populate_review_fields_2(self):
      review2 = '''
        <div class="col-lg-9 col-sm-8 col-xs-12 reviewDetail">
        <p class="reviewTitle">Lorem ipsum</p>
        <p class="reviewText"><br/>Its was easy to do, he agent was very helpful and the money was there the next morning so that was a big help<br/></p>
        <div aria-hidden="true" class="hideText">
        <p class="consumerName">John Doe                                                                      <span>from BEL AIR, MD</span></p>
        <p class="consumerReviewDate">Reviewed in April 2019</p>
        </div>
        <div class="helpfull-count desktop-view">
        <div class="helpfull-section">
        <input class="reviewId" name="reviewId" type="hidden" value="5e4c78ae13c6370001bb56f5"/>
        <div class="flagged-review">
        <button aria-label="Mark this review as flagged" class="flag" id="flag-5e4c78ae13c6370001bb56f5">
        <div class="flag-content">
        <img alt="" src="https://www.lendingtree.com/content/themes/lt-wp-www-theme/dist/images/lender-review/review-flag-desktop.png"/>
        <span class="flag-text">Flag review</span>
        </div>
        </button>
        </div>
        </div>
        </div>
        </div>
      '''

      review_2_as_soup = BeautifulSoup(review2, 'html.parser')

      output_2 = populate_review_fields(review_2_as_soup, 3)

      self.assertTrue('value' in output_2)
      self.assertTrue('name' in output_2)
      self.assertTrue('title' in output_2)
      self.assertTrue('date' in output_2)
      self.assertTrue('stars' in output_2)
      self.assertEqual(output_2['date'], "Reviewed in April 2019")
      self.assertEqual(output_2['name'], "John Doe")
      self.assertEqual(output_2['title'], "Lorem ipsum")
      self.assertEqual(output_2['value'], "Its was easy to do, he agent was very helpful and the money was there the next morning so that was a big help")
      self.assertEqual(output_2['stars'], 3)

    def test_reviews_are_equal_true_case(self):
      review_1 = {}
      review_2 = {}

      review_1["name"] = "Adam"
      review_2["name"] = "Adam"

      review_1["title"] = "The title"
      review_2["title"] = "The title"

      review_1["value"] = "val 1"
      review_2["value"] = "val 1"

      review_1["stars"] = 2
      review_2["stars"] = 2

      review_1["date"] = "February 2020"
      review_2["date"] = "February 2020"

      bool_1 = reviews_are_equal(review_1, review_2)

      self.assertTrue(bool_1)

if __name__ == '__main__':
    unittest.main()

# flattened = [
        # {"date":"Reviewed in February 2020","name":"Danny","stars":2,"title":"It was nice to talk to someone who really took time for me","value":"It was kinda frustrating because I've havnt received my loan yet. And I need to now would Samsung pay would work , because I found out my card from member one is deactivated."},
        # {"date":"Reviewed in February 2020","name":"James","stars":2,"title":"aPPROVAL WAS QUICK, CASH, DESPITE ADVERTISING 'SAME DAY' WAS not (1 WEEK??? Whaaat???)","value":"Internet accessibility was confusing, impossible w/o phone assistance!  Very baaad!!!  poorly thought out!"},
        # {"date":"Reviewed in January 2020","name":"Alicia","stars":2,"title":"Loan","value":"I got approved for a loan then later decided. CashNetUsa full of bs. I really thought I had the loan."},
        # {"date":"Reviewed in September 2019","name":"Jesse","stars":2,"title":"It was an easy experience","value":"The process was easy ,quick and excellant. I am hoping that rates drop in the future for people needing assistance but not having to pay so high an interest rate."},
        # {"date":"Reviewed in September 2019","name":"DOTTIE","stars":2,"title":"Its convenient!","value":"I am a single mother of 4. I have a sister and her 3 kids having to evacuate her home due to hurrican Dorian. I am not well off as most are and I needed to help my sister with funds. I reach out to you. I am thankful that you were so convient at the time. however, I think it is absolutely degrading to be able to charge the outrageous interest as this company does. Its greedy and evil! The LOVE of money is the root of all evil. Point being, it's the ones having to come ask for help on things they need in the first place. What logical sense does it make to charge double what you asked to borrow. I dont know how you snakes sleep at night.  Thank you again for convenience."},
        # {"date":"Reviewed in August 2019","name":"Laura","stars":2,"title":"Loan","value":"Yes I got the loan now I am having severe regrets ."},
        # {"date":"Reviewed in February 2020","name":"Danny","stars":2,"title":"It was nice to talk to someone who really took time for me","value":"It was kinda frustrating because I've havnt received my loan yet. And I need to now would Samsung pay would work , because I found out my card from member one is deactivated."},
        # {"date":"Reviewed in February 2020","name":"James","stars":2,"title":"aPPROVAL WAS QUICK, CASH, DESPITE ADVERTISING 'SAME DAY' WAS not (1 WEEK??? Whaaat???)","value":"Internet accessibility was confusing, impossible w/o phone assistance!  Very baaad!!!  poorly thought out!"},
        # {"date":"Reviewed in January 2020","name":"Alicia","stars":2,"title":"Loan","value":"I got approved for a loan then later decided. CashNetUsa full of bs. I really thought I had the loan."},
        # {"date":"Reviewed in September 2019","name":"Jesse","stars":2,"title":"It was an easy experience","value":"The process was easy ,quick and excellant. I am hoping that rates drop in the future for people needing assistance but not having to pay so high an interest rate."},
        # {"date":"Reviewed in September 2019","name":"DOTTIE","stars":2,"title":"Its convenient!","value":"I am a single mother of 4. I have a sister and her 3 kids having to evacuate her home due to hurrican Dorian. I am not well off as most are and I needed to help my sister with funds. I reach out to you. I am thankful that you were so convient at the time. however, I think it is absolutely degrading to be able to charge the outrageous interest as this company does. Its greedy and evil! The LOVE of money is the root of all evil. Point being, it's the ones having to come ask for help on things they need in the first place. What logical sense does it make to charge double what you asked to borrow. I dont know how you snakes sleep at night.  Thank you again for convenience."},
        # {"date":"Reviewed in August 2019","name":"Laura","stars":2,"title":"Loan","value":"Yes I got the loan now I am having severe regrets ."},
        # ]
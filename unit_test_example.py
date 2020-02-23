import unittest
from review_field_utils import populate_review_fields, construct_url_prefix, parse_reviews
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

if __name__ == '__main__':
    unittest.main()
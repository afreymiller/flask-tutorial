import unittest
from review_field_utils import populate_review_fields, construct_url, parse_response_for_reviews

# https://docs.python.org/3/library/unittest.html

class TestStringMethods(unittest.TestCase):

    def test_construct_url_1(self):
      expected_url_1 = "https://www.lendingtree.com/reviews/personal/cashnetusa/81638970?OverallRating=1&pid=1"
      self.assertEqual(construct_url('cashnetusa', '81638970'), expected_url_1)

    def test_construct_url_2(self):
      expected_url_1 = "https://www.lendingtree.com/reviews/personal/cashnetusa/81638970?OverallRating=1&pid=1"
      
      with self.assertRaises(ValueError) as context:
            construct_url('cashnetusa', 'abc')

      self.assertTrue('Input for review_id should be an integer' in str(context.exception))
      
    def test_construct_url_3(self):
      expected_url_1 = "https://www.lendingtree.com/reviews/personal/cashnetusa/81638970?OverallRating=1&pid=1"
      
      with self.assertRaises(AttributeError) as context:
            construct_url(3, '1234123')

      self.assertTrue('Input for lender should be a non-null string' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
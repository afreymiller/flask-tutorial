import unittest
from review_field_utils import populate_review_fields, construct_url, parse_response_for_reviews

# https://docs.python.org/3/library/unittest.html

class TestStringMethods(unittest.TestCase):

    def test_construct_url_1(self):
      expected_url_1 = "https://www.lendingtree.com/reviews/personal/cashnetusa/81638970?OverallRating=1&pid=1"
      self.assertEqual(construct_url('cashnetusa', '81638970'), expected_url_1)

    def test_construct_url_2(self):      
      with self.assertRaises(ValueError) as context:
            construct_url('cashnetusa', 'abc')

      self.assertTrue('review_id should be a non-negative integer.' in str(context.exception))
      
    def test_construct_url_3(self):
      
      with self.assertRaises(TypeError) as context:
            construct_url(3, '1234123')

      self.assertTrue('Input for lender should be a string' in str(context.exception))

    def test_construct_url_4(self):      
      with self.assertRaises(RuntimeError) as context:
            construct_url("", '1234123')

      self.assertTrue('Lender must be non-null' in str(context.exception))

    def test_construct_url_5(self):
      
      with self.assertRaises(ValueError) as context:
            construct_url('cashnetusa', '-5')

      self.assertTrue('review_id should be a non-negative integer.' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
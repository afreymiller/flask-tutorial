import unittest
from review_field_utils import populate_review_fields, construct_url, parse_response_for_reviews

# https://docs.python.org/3/library/unittest.html

class TestStringMethods(unittest.TestCase):

    def test_construct_url(self):
      expected_url_1 = "https://www.lendingtree.com/reviews/personal/cashnetusa/81638970?OverallRating=1&pid=1"
      self.assertEqual(construct_url('cashnetusa', '81638970'), expected_url_1)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
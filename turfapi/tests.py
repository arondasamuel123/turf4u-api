from django.test import TestCase


class BasicTestCase(TestCase):

    def test_addition(self):
        add = 1+2

        self.assertEqual(add, 3)

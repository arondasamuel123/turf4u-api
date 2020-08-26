from django.test import TestCase


class BasicTestCase(TestCase):

    def test_addition(self):
        add = 1+2

        self.assertEqual(add, 3)

    def test_subtraction(self):
        subtract = 4-1
        self.assertEqual(subtract, 3)

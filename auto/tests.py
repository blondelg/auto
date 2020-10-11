from django.test import TestCase
import requests


class GeneralTestCase(TestCase):

    def test_network(self):

        self.assertEqual(requests.get("https://google.fr").status_code, 200)


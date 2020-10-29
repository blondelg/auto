from django.test import TestCase
from django.conf import settings
import requests


class GeneralTestCase(TestCase):

    def test_network(self):

        self.assertEqual(requests.get("https://google.fr").status_code, 200)

    def test_database(self):

        pass

    def test_parameters_max_proxy_try(self):
        p = settings.CONFIG['SCRAPPER']['max_proxy_try']
        self.assertIsInstance(p, str)

    def test_parameters_session_timeout(self):
        p = settings.CONFIG['SCRAPPER']['session_timeout']
        self.assertIsInstance(p, str)

    def test_parameters_min_sleep_time(self):
        p = settings.CONFIG['SCRAPPER']['min_sleep_time']
        self.assertIsInstance(p, str)

    def test_parameters_max_sleep_time(self):
        p = settings.CONFIG['SCRAPPER']['max_sleep_time']
        self.assertIsInstance(p, str)

    def test_parameters_ENGINE(self):
        p = settings.CONFIG['DATABASE']['ENGINE']
        self.assertIsInstance(p, str)

    def test_parameters_(self):
        p = settings.CONFIG['DATABASE']['NAME']
        self.assertIsInstance(p, str)

    def test_parameters_(self):
        p = settings.CONFIG['DATABASE']['USER']
        self.assertIsInstance(p, str)

    def test_parameters_(self):
        p = settings.CONFIG['DATABASE']['PASSWORD']
        self.assertIsInstance(p, str)

    def test_parameters_(self):
        p = settings.CONFIG['DATABASE']['HOST']
        self.assertIsInstance(p, str)

    def test_parameters_(self):
        p = settings.CONFIG['DATABASE']['PORT']
        self.assertIsInstance(p, str)

    def test_parameters_(self):
        p = settings.CONFIG['GENERAL']['SECRET_KEY']
        self.assertIsInstance(p, str)

    def test_parameters_(self):
        p = settings.CONFIG['GENERAL']['LOG_BACKUP_DAYS']
        self.assertIsInstance(p, str)

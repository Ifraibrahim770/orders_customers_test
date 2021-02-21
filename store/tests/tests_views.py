from django.test import TestCase, Client
from django.urls import reverse
import os


class TestViews(TestCase):

    def set_up(self):
        self.client = Client()
        self.sign_in_url = reverse('sign_in')
        self.add_cust_url = 'AddCustomer'

    def test_sign_in_view(self):
        response = self.client.get(reverse('sign_in'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainpage.html')
        print(os.environ.get('IBRAHIM'))

    def test_add_customer(self):
        response = self.client.get(reverse('AddCustomer'), {'Name': 'TESTNAME', 'Phone': '074145514'})
        self.assertEquals(response.status_code, 200)


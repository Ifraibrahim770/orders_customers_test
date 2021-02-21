from django.test import SimpleTestCase
from django.urls import reverse, resolve

from store.views import AddOrder, AddCustomer, sign_in


class TestUrls(SimpleTestCase):

    def test_make_order_url(self):
        url = reverse('MakeOrder')
        self.assertEquals(resolve(url).func.view_class,AddOrder)

    def test_add_customer_url(self):
        url = reverse('AddCustomer')
        self.assertEquals(resolve(url).func.view_class, AddCustomer)

    def test_sign_in_url(self):
        url = reverse('sign_in')
        self.assertEquals(resolve(url).func, sign_in)
from django.test import TestCase, RequestFactory

from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
from ..models import Order, Item
from ..views import BuyOrderView, OrderView


class BuyOrderViewTest(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.item = Item.objects.create(name='Test Item', description='Test Description', price=100.00)
        self.order = Order.objects.create()
        self.order.items.add(self.item)

    @patch('stripe.PaymentIntent.create')
    def test_buy_order_view(self, mock_create):
        mock_create.return_value = {'client_secret': 'secret123'}
        response = self.client.get(reverse('buy_order', kwargs={'id': self.order.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'client_secret': 'secret123'})


class OrderViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.item = Item.objects.create(name='Test Item', description='Test Description', price=100.00)
        self.order = Order.objects.create()
        self.order.items.add(self.item)

    def test_order_view(self):
        request = self.factory.get(reverse('order', kwargs={'id': self.order.id}))
        response = OrderView.as_view()(request, id=self.order.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')

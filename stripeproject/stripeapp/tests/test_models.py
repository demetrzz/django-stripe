from django.test import TestCase
from ..models import Item, Order, OrderItem, Discount, Tax


class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name='Test Item', description='Test Description', price=100.00)

    def test_item_creation(self):
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(self.item.name, 'Test Item')


class OrderModelTest(TestCase):
    def setUp(self):
        self.item1 = Item.objects.create(name='Test Item 1', description='Test Description 1', price=100.00)
        self.item2 = Item.objects.create(name='Test Item 2', description='Test Description 2', price=200.00)
        self.order = Order.objects.create()
        self.order.items.add(self.item1, self.item2)

    def test_order_creation(self):
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.items.count(), 2)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name='Test Item', description='Test Description', price=100.00)
        self.order = Order.objects.create()
        self.order_item = OrderItem.objects.create(order=self.order, item=self.item, quantity=2)

    def test_order_item_creation(self):
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.quantity, 2)


class DiscountModelTest(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(name='Test Discount', amount=10.00)

    def test_discount_creation(self):
        self.assertEqual(Discount.objects.count(), 1)
        self.assertEqual(self.discount.name, 'Test Discount')


class TaxModelTest(TestCase):
    def setUp(self):
        self.tax = Tax.objects.create(name='Test Tax', amount=5.00)

    def test_tax_creation(self):
        self.assertEqual(Tax.objects.count(), 1)
        self.assertEqual(self.tax.name, 'Test Tax')

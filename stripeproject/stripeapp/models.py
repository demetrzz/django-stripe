from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem')
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True)

    @property
    def total_amount(self):
        total = sum(order_item.item.price * order_item.quantity for order_item in self.orderitem_set.all())
        if self.discount:
            total -= total * (self.discount.amount / 100)
        if self.tax:
            total += total * (self.tax.amount / 100)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Discount(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=4, decimal_places=2)  # This is the discount percentage


class Tax(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=4, decimal_places=2)  # This is the tax percentage

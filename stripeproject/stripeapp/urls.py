from django.urls import path
from .views import BuyOrderView, OrderView

urlpatterns = [
    path('buy/order/<int:id>/', BuyOrderView.as_view(), name='buy_order'),
    path('order/<int:id>/', OrderView.as_view(), name='order'),
]

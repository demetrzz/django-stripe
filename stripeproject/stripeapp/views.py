from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
import stripe
from rest_framework.views import APIView

from .models import Order


class BuyOrderView(APIView):
    def get(self, request, **kwargs):
        order = get_object_or_404(Order, id=kwargs['id'])
        stripe.api_key = settings.STRIPE_SECRET_KEY

        total_amount = order.total_amount

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),
                currency='usd',
                payment_method_types=['card'],
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'client_secret': intent['client_secret']})


class OrderView(View):
    def get(self, request, **kwargs):
        order = get_object_or_404(Order, id=kwargs['id'])
        context = {
            'order': order,
            'total_amount': order.total_amount,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, 'order.html', context)

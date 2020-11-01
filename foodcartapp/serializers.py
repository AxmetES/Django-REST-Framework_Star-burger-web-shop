from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Order, OrderDetails


class OrderDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderDetailsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'address', 'phonenumber', 'products']

    def validate_products(self, value):
        if not value:
            raise ValidationError('product field is empty.')
        return value

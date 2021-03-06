import decimal

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderDetails
from .serializers import OrderSerializer


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@transaction.atomic()
@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order, is_created = Order.objects.update_or_create(firstname=serializer.validated_data['firstname'],
                                                       lastname=serializer.validated_data['lastname'],
                                                       phonenumber=serializer.validated_data['phonenumber'],
                                                       address=serializer.validated_data['address'], )

    for product_item in serializer.validated_data['products']:
        order_detail, is_created = OrderDetails.objects.get_or_create(product=product_item['product'],
                                                                      order=order,
                                                                      defaults={
                                                                          'quantity': product_item['quantity'],
                                                                          'product_price': product_item[
                                                                                               'product'].price *
                                                                                           product_item['quantity']})
        if not is_created:
            order_detail.quantity = order_detail.quantity + product_item['quantity']
            order_detail.product_price = order_detail.product_price + float((
                product_item['product'].price * product_item['quantity']))
            order_detail.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)

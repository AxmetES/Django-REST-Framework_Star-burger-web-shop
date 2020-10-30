from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderDetails


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


@api_view(['POST'])
def register_order(request):
    print('------------------->>')
    # if isinstance(order_info, dict) and 'products' in order_info.keys() and isinstance(order_info['products'],
    #                                                                                    list) and order_info[
    #     'products'] and isinstance(order_info['firstname'], str) and 'firstname' :
    try:
        order_info = request.data
        if not order_info["products"]:
            raise TypeError
        if order_info['phonenumber'] == '':
            raise ValueError
        if not isinstance(order_info['firstname'], str):
            raise TypeError

        order, is_created = Order.objects.update_or_create(name=order_info['firstname'],
                                                           last_name=order_info['lastname'],
                                                           phone_number=order_info['phonenumber'],
                                                           address=order_info['address'])

        for product_item in order_info['products']:
            product = get_object_or_404(Product, id=product_item['product'])
            order_detail, is_created = OrderDetails.objects.get_or_create(product=product, order=order,
                                                                          defaults={
                                                                              'quantity': product_item['quantity']})

            if not is_created:
                order_detail.quantity = order_detail.quantity + product_item['quantity']
                order_detail.save()
            return Response(status=status.HTTP_200_OK)
    except (TypeError, KeyError, IntegrityError, ValueError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

# {"products":  [{"product": 2, "quantity": 2}], "firstname": "1", "lastname": "2", "phonenumber": "3", "address": "4"}

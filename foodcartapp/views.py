import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static

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


def register_order(request):
    try:
        order_info = json.loads(request.body.decode())
    except ValueError:
        return JsonResponse({
            'error': 'Order info request not received.',
        })
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
            # current_quantity =
            order_detail.quantity = order_detail.quantity + product_item['quantity']
            order_detail.save()

    return JsonResponse({})

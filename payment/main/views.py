from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Item, Order, Coupon
from decouple import config
import stripe


def item_list(request):
    """
    Получение списка товаров
    :param request: объект запроса
    :return: html-страница со списком товаров
    """
    item_list = Item.objects.all()
    return render(request, 'main/item_list.html', {'item_list': item_list})


def item(request, id):
    """
    Получение товара
    :param request: объект запроса
    :param id: идентификатор товара
    :return: html-страница с запрашиваемым товаром
    """
    if Item.objects.filter(pk=id).exists():
        item = Item.objects.get(pk=id)
        return render(request, 'main/item.html', {'item': item})
    return JsonResponse({'error': 'item id=' + str(id) + ' not found'})


def get_striple_config(request):
    """
    Получение публичного api-ключа
    :param request: объект запроса
    :return: Публичный api-ключ
    """
    if request.method == 'GET':
        stripe_config = {'publicKey': config('STRIPE_PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config)


def buy(request, id):
    """
    Оплата товара
    :param request: объект запроса
    :param id: идентификатор товара
    :return: идентификатор сессии оплаты товара
    """
    if request.method == 'GET':
        domain_url = config('DOMAIN_URL')
        stripe.api_key = config('STRIPE_SECRET_KEY')
        try:
            if Item.objects.filter(pk=id).exists():
                item = Item.objects.get(pk=id)
                session = stripe.checkout.Session.create(
                    line_items=[{
                        'price_data': {
                            'currency': 'rub',
                            'product_data': {
                                'name': item.name,
                            },
                            'unit_amount': int(item.price * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=domain_url + '/success/',
                    cancel_url=domain_url + '/cancel',
                )
            else:
                return JsonResponse({'error': 'item id=' + str(id) + ' not found'})
            return JsonResponse({'sessionId': session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def success(request):
    """
    Рендер страницы успешной оплаты товара
    :param request: объект запроса
    :return: html-страница успешной оплаты товара
    """
    return render(request, 'main/success.html')


def cancel(request):
    """
    Рендер страницы неуспешной оплаты товара
    :param request: объект запроса
    :return: html-страница неуспешной оплаты товара
    """
    return render(request, 'main/cancel.html')


def add_item_to_order(request, id):
    """
    Добавление товара к заказу
    :param request: объект запроса
    :param id: идентификатор товара
    :return: пустой ответ
    """
    if request.method == 'GET':
        if not request.session.get('order', []) or not Order.objects.filter(pk=request.session['order']).exists():
            order = Order.objects.create()
            request.session['order'] = order.id
        else:
            order = Order.objects.get(id=request.session['order'])
        order.items.add(Item.objects.get(id=id))
        return HttpResponse()


def order(request):
    """
    Получение заказа
    :param request: объект запроса
    :return: html-страница с запрашиваемым заказом
    """
    if request.method == 'GET':
        if request.session.get('order', []) and Order.objects.filter(pk=request.session['order']).exists():
            order = Order.objects.get(pk=request.session['order'])
        else:
            order = None
        coupon_list = Coupon.objects.all()
        data = {'order': order,
                'coupon_list': coupon_list}
        return render(request, 'main/order.html', data)


def order_pay(request, id, coupon_id):
    """
    Оплата заказа
    :param request: объект запроса
    :param id: идентификатор заказа
    :param coupon_id: идентификатор купона
    :return: идентификатор сессии оплаты заказа
    """
    if request.method == 'GET':
        domain_url = config('DOMAIN_URL')
        stripe.api_key = config('STRIPE_SECRET_KEY')
        try:
            if Order.objects.filter(pk=id).exists():
                order = Order.objects.get(pk=id)
                order.is_paid = True
                order.save()
                request.session['order'] = []
                if coupon_id == '-1' or not Coupon.objects.filter(pk=coupon_id).exists():
                    coupon = None
                else:
                    coupon = Coupon.objects.get(pk=coupon_id).coupon_code
                items = [{'price_data': {
                            'currency': 'rub',
                            'product_data': {
                                'name': item.name,
                            },
                            'unit_amount': int(item.price * 100),
                        },
                        'quantity': 1} for item in order.items.all()]
                session = stripe.checkout.Session.create(
                    line_items=items,
                    mode='payment',
                    discounts=[{
                        'coupon': coupon,
                    }],
                    success_url=domain_url + '/success',
                    cancel_url=domain_url + '/cancel',
                )
            else:
                return JsonResponse({'error': 'item id=' + str(id) + ' not found'})
            return JsonResponse({'sessionId': session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def generate_coupon(request, percent_off):
    """
    Создание купона
    :param request: объект запроса
    :param percent_off:
    :return: код купона
    """
    stripe.api_key = config('STRIPE_SECRET_KEY')
    if Coupon.objects.filter(percent_off=percent_off).exists():
        cpn = Coupon.objects.get(percent_off=percent_off)
    else:
        coupon = stripe.Coupon.create(percent_off=percent_off, duration="forever")
        cpn = Coupon.objects.create(percent_off=coupon['percent_off'], coupon_code=coupon['id'])
    return JsonResponse({'coupon': cpn.coupon_code})
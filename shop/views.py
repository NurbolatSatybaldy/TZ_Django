from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.conf import settings
import stripe
from .models import Item, Order


def index(request):
    """Главная страница со списком товаров"""
    try:
        items = Item.objects.all()
        context = {'items': items}
        return render(request, 'shop/index.html', context)
    except Exception as e:
        # Логируем ошибку для отладки
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Ошибка на главной странице: {str(e)}")
        from django.http import HttpResponse
        return HttpResponse(f"Ошибка сервера. Проверьте логи. {str(e)}", status=500)


def success_page(request):
    """Страница успешной оплаты"""
    return render(request, 'shop/success.html')


def cancel_page(request):
    """Страница отмены оплаты"""
    return render(request, 'shop/cancel.html')


def get_secret_key(curr):
    """Возвращает секретный ключ Stripe в зависимости от валюты"""
    if curr == "RUB":
        return settings.STRIPE_SECRET_KEY_RUB
    return settings.STRIPE_SECRET_KEY_USD


def get_pub_key(curr):
    """Возвращает публичный ключ Stripe в зависимости от валюты"""
    if curr == "RUB":
        return settings.STRIPE_PUBLISHABLE_KEY_RUB
    return settings.STRIPE_PUBLISHABLE_KEY_USD


def item_detail(request, id):
    """Отображает страницу товара с кнопкой покупки"""
    try:
        item = get_object_or_404(Item, id=id)
    except Http404:
        return JsonResponse({"error": "Товар не найден"}, status=404)

    pub_key = get_pub_key(item.currency)
    
    if not pub_key or pub_key.startswith('pk_test_51QEXAMPLE') or len(pub_key) < 20:
        return JsonResponse(
            {"error": "Stripe ключ не настроен или недействителен. Пожалуйста, добавьте реальные ключи из Stripe Dashboard в файл .env"},
            status=500
        )

    context = {
        'item': item,
        'stripe_publishable_key': pub_key,
    }
    return render(request, 'shop/item_detail.html', context)


def buy_item(request, id):
    """Создает Stripe Checkout Session для покупки товара"""
    from django.http import HttpResponseRedirect
    
    try:
        item = get_object_or_404(Item, id=id)
    except Http404:
        return JsonResponse({"error": "Товар не найден"}, status=404)

    secret_key = get_secret_key(item.currency)
    
    if not secret_key or secret_key.startswith('sk_test_51QEXAMPLE') or len(secret_key) < 20:
        return JsonResponse(
            {"error": "Stripe ключ не настроен или недействителен. Пожалуйста, добавьте реальные ключи из Stripe Dashboard в файл .env"},
            status=500
        )

    stripe.api_key = secret_key

    try:
        # Создаем сессию Stripe Checkout согласно документации
        # https://docs.stripe.com/payments/accept-a-payment?integration=checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency.lower(),
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        
        # Если запрос через AJAX/fetch, возвращаем JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'id': session.id, 'url': session.url})
        
        # Иначе редиректим напрямую на Checkout (как в документации)
        return HttpResponseRedirect(session.url)
        
    except stripe.error.StripeError as e:
        return JsonResponse(
            {"error": f"Ошибка Stripe: {str(e)}"},
            status=500
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Внутренняя ошибка сервера: {str(e)}"},
            status=500
        )


def buy_order(request, id):
    """Создает Stripe Checkout Session для покупки заказа"""
    try:
        order = get_object_or_404(Order, id=id)
    except Http404:
        return JsonResponse({"error": "Заказ не найден"}, status=404)

    items = order.items.all()
    if not items.exists():
        return JsonResponse({"error": "Заказ не содержит товаров"}, status=400)

    curr = order.get_currency()
    secret_key = get_secret_key(curr)
    
    if not secret_key:
        return JsonResponse(
            {"error": "Stripe ключ не настроен для данной валюты"},
            status=500
        )

    stripe.api_key = secret_key

    try:
        line_items = []
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': item.currency.lower(),
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            })

        params = {
            'payment_method_types': ['card'],
            'line_items': line_items,
            'mode': 'payment',
            'success_url': request.build_absolute_uri('/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            'cancel_url': request.build_absolute_uri('/cancel/'),
        }

        if order.discount:
            params['discounts'] = [{
                'coupon': order.discount.coupon_id
            }]

        if order.tax:
            for li in line_items:
                li['tax_rates'] = [order.tax.tax_rate_id]

        session = stripe.checkout.Session.create(**params)
        return JsonResponse({'id': session.id})
    except stripe.error.StripeError as e:
        return JsonResponse(
            {"error": f"Ошибка Stripe: {str(e)}"},
            status=500
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Внутренняя ошибка сервера: {str(e)}"},
            status=500
        )


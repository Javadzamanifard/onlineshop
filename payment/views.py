from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.urls import reverse

import requests

from config import settings
from orders.models import Order

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id = order_id)
    
    price_toman = order.get_total_cost()
    price_rial = price_toman * 10
    
    if not order_id:
        # اگر شناسه سفارشی وجود نداشت، کاربر را به جایی منطقی هدایت کنید
        return redirect('cart:cart_detail') # مثلا به سبد خرید
    
    
    ## For zarinpal
    req_headers = {
        'accept' : 'application/json',
        'content-type' : 'application/json',
    }
    
    req_data = {
        'merchant_id' : settings.ZARINPAL_MERCHANT_ID, 
        'amount' : price_rial,
        'description' : f'#{order.id} by {order.first_name} {order.last_name}',
        'callback_url' : request.build_absolute_url(reverse('payment:payment_callback')),
    }
    
    ZARINPAL_REQUEST_URL = 'https://payment.zarinpal.com/pg/v4/payment/request.json'
    response = requests.post(url = ZARINPAL_REQUEST_URL, json = req_data, headers = req_headers)
    
    data = response.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()
    
    if 'errors' not in data and len(data['errors']) == 0:
        return redirect('https://payment.zarinpal.com/pg/StartPay/{authority}'.format(authority = authority))
    else:
        return HttpResponse('خطا از طرف زرین پال')


def payment_callback(request):
    payment_authority = request.GET.get['authority']
    payment_status = request.GET.get['code']
    
    order = get_object_or_404(Order, zarinpal_authority = payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10
    
    if payment_status == 'ok':
        req_headers = {
        'accept' : 'application/json',
        'content-type' : 'application/json',
        }
        
        req_data = {
        'merchant_id' : settings.ZARINPAL_MERCHANT_ID,
        'amount' : rial_total_price,
        'authority' : payment_authority,
        }  
        
        ZARINPAL_VERIFY_URL = 'https://payment.zarinpal.com/pg/v4/payment/verify.json'
        response = requests.post(url = ZARINPAL_VERIFY_URL, json = req_data, headers = req_headers)
        
        # if response.json().get['data'] and ('errors' not in response.json()['data'] or len(response.json()['data']['errors']) == 0 ):
        if 'data' in response.json() and ('errors' not in response.json()['data'] or len(response.json()['data']['errors']) == 0 ):
            data = response.json()['data']
            payment_code = data['code']
            
            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()
                
                return HttpResponse('پرداخت با موفقیت انجام گرفت')
            
            elif payment_code == 101:
                return HttpResponse('تراکنش قبلا ثبت شده است')
            
            else:
                error_code = response.json()['errors']['code']
                error_msg = response.json()['errors']['message']
                return HttpResponse(f'{error_msg}{error_code}تراکنش ناموفق')
    else:
        return HttpResponse('تراکنش ناموفق')
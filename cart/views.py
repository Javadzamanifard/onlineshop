from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone

from .cart import Cart
from .models import Coupon
from products.models import Product
from .forms import CartForm, CouponForm

def cart_detail(request):
    cart = Cart(request)
    form = CouponForm(request.POST or None)
    coupon = None
    discount_amount = 0
    total_price = cart.get_total_price()
    price_after_discount = total_price
    
    
    for item in cart:
        item['update_quantity_override_quantity_form'] = CartForm(
            initial = {
                        'quantity' : item['quantity'],
                        'override_quantity' : True, 
                        }
        )
    
    if request.method == 'POST':
        now = timezone.now()
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(
                                            code__iexact=code,
                                            active=True,
                                            valid_from__lte=now,
                                            valid_to__gte=now
            )
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
        
        coupon_id = request.session['coupon_id']
        if coupon_id:
            coupon = get_object_or_404(Coupon, id=coupon_id)
            if coupon.is_valid():
                discount_amount = coupon.get_discount_amount(total_price)
                price_after_discount = coupon.apply_discount(total_price)
            
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'coupon_form': form,
        'coupon': coupon,
        'discount' : discount_amount,
        'total_price_after_discount': price_after_discount
    })


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    form = CartForm(request.POST)
    if form.is_valid():
        cleand_data = form.cleaned_data
        quantity = cleand_data['quantity']
        override_quantity = cleand_data['override_quantity']
        # cart.add(product, quantity, override_quantity = cleand_data['override_quantity'])
        cart.add(product, quantity, override_quantity)
    
    return redirect('cart:cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    cart.remove(product = product)
    return redirect('cart:cart_detail')

@require_POST
def clear_cart(request):
    cart = Cart(request)
    # del cart
    cart.clear()
    return redirect('product_list')

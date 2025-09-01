from django.shortcuts import render, redirect

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem

def order_create_view(request):
    cart = Cart(request)
    order_form = OrderCreateForm()
    
    if len(cart) == 0:
        return redirect('list_view')
        
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            new_order_form = order_form.save(commit = False)
            new_order_form.user = request.user
            new_order_form.save()
            
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order = new_order_form,
                    product = product,
                    quantity = item['quantity'],
                    price = product.price,
                )
                
            cart.clear()
            
            request.user.first_name = new_order_form.first_name
            request.user.last_name = new_order_form.last_name
            request.user.save()
            
            ## For payment 
            request.session['order_id'] = new_order_form.id
            return redirect('payment:payment_process')
            
    return render(request, 'orders/order_create.html', context = {
        'order_form' : order_form,
    })
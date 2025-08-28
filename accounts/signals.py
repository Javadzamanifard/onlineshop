from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from cart.models import Cart, CartItem
from cart.cart import Cart as SessionCart

@receiver(user_logged_in)
def merge_session_cart_to_db_cart(sender, request, user, **kwargs):
    session_cart = SessionCart(request)
    if len(session_cart) > 0:
        db_cart, created = Cart.objects.get_or_create(user=user)
        
        for item in session_cart:
            product = item['product']
            quantity = item['quantity']
            
            # بررسی اینکه آیا این محصول قبلا در سبد دیتابیس وجود دارد
            db_item, item_created = CartItem.objects.get_or_create(
                cart=db_cart,
                product=product,
                defaults={'unit_price': item['price']}
            )

            if not item_created:
                # اگر وجود داشت، تعداد را اضافه می‌کنیم
                db_item.quantity += quantity
            else:
                # اگر جدید بود، تعداد را تنظیم می‌کنیم
                db_item.quantity = quantity
            db_item.save()
            
        # پاک کردن سبد خرید از session
        session_cart.clear()
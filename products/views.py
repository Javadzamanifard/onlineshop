from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Product, Category, Comment, WishList

from .forms import CommentForm, SearchForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'  # نام متغیر در تمپلیت
    paginate_by = 4                   # صفحه‌بندی

    def get_context_data(self, **kwargs):
    # 1. ابتدا context پیش‌فرض را از کلاس پدر (ListView) می‌گیریم
        context = super().get_context_data(**kwargs)

        # 2. حالا اطلاعات دلخواه خودمان را به آن اضافه می‌کنیم
        user_wishlist_ids = []
        # چک می‌کنیم که آیا کاربر لاگین کرده است یا نه
        if self.request.user.is_authenticated:
            # اگر لاگین کرده بود، لیست ID محصولاتی که در wishlist او هست را استخراج می‌کنیم
            user_wishlist_ids = list(WishList.objects.filter(user=self.request.user).values_list('product_id', flat=True))
        # 3. لیست IDها را به context اضافه می‌کنیم
        context['user_wishlist_ids'] = user_wishlist_ids
        
        # 4. در نهایت context جدید و کامل شده را برمی‌گردانیم
        return context


    def get_queryset(self):
        """
        این متد queryset اصلی را بازنویسی می‌کند تا منطق جستجو را اضافه کند.
        """
        # ابتدا queryset پیش‌فرض را می‌گیریم (که معادل Product.objects.all() است)
        
        queryset = super().get_queryset()
        
        # عبارت جستجو شده را از پارامتر GET در URL می‌خوانیم
        query = self.request.GET.get('search')
            
        if query:
            # ۱. عبارت جستجو را به لیستی از کلمات کلیدی تبدیل می‌کنیم
            # مثلاً "کفش ادیداس" تبدیل می‌شود به ['کفش', 'ادیداس']
            keywords = query.split()
            # ۲. یک فیلتر Q اولیه و خالی می‌سازیم تا شرایط را به آن اضافه کنیم
            combined_q = Q()
                        # ۳. برای هر کلمه کلیدی، یک شرط به فیلتر اصلی AND می‌کنیم
            for kw in keywords:
                combined_q &= (
                    Q(name__icontains=kw) | Q(description__icontains=kw)
                )
            # اگر عبارتی برای جستجو وجود داشت، queryset را فیلتر می‌کنیم
            return queryset.filter(combined_q)
        
        # اگر جستجویی در کار نبود، همان queryset کامل را برمی‌گردانیم
        return queryset

    def get_context_data(self, **kwargs):
        """
        این متد context را بازنویسی می‌کند تا فرم جستجو را به آن اضافه کند.
        """
        # ابتدا context پیش‌فرض را از کلاس پدر می‌گیریم
        context = super().get_context_data(**kwargs)
        
        # فرم جستجو را به context اضافه می‌کنیم تا در تمپلیت قابل استفاده باشد
        # مقدار اولیه فرم را با چیزی که کاربر جستجو کرده پر می‌کنیم
        context['form'] = SearchForm(self.request.GET or None)
        
        return context


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'products/product_detail.html'
#     context_object_name = 'product'
#     # slug_field و slug_url_kwarg را برای استفاده از اسلاگ در URL مشخص می‌کنیم
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'
#     form_class = CommentForm
    
#     def get_success_url(self):
#         return self.request.path
    
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valiud(form)
#         return self.form_invalid(form)
    
#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.product = self.object
#         if self.request.user.is_authenticated:
#             comment.user = self.request.user
#         comment.save()
#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         return self.render_to_response(
#             self.get_context_data(form=form)
#         )
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # اگر متد post فرم خطا داده باشد، از آن استفاده می‌کنیم
#         # context['form'] = kwargs.get('form', self.get_form())
#         context['form'] = CommentForm()
#         context['comments'] = Comment.objects.filter(
#             is_active =True,
#         ).order_by('-created_at')
#         return context

@login_required
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk = pk)
    product_comments = product.comments.filter(is_active = True, parent__isnull=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.product = product
            
            if request.user.is_authenticated:
                new_form.user = request.user
                new_form.guest_name  = None
                
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id, product=product).first()
                if parent_comment:
                    new_form.parent = parent_comment
                    
            new_form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = CommentForm(initial = {
            'parent' : request.GET.get('parent')
        })
    
    print(f"تعداد کامنت‌ها برای ارسال به تمپلیت: {product.comments.count()}")
    print(f"آیا فرم ساخته شده است؟ {form is not None}")
    context={
        'product' : product,
        'comments' : product_comments,
        'form' : form,
    }
    return render(request, 'products/product_detail.html', context)



@login_required # این دکوریتور اجازه نمی‌دهد کاربر لاگین نکرده به این ویو دسترسی داشته باشد
def toggle_wishlist_view(request):
    # اطمینان حاصل می‌کنیم که درخواست از نوع POST است
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است'})

    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'شناسه محصول ارسال نشده است'})

    product = get_object_or_404(Product, id=product_id)
    
    # اصل منطق اینجاست:
    # get_or_create: سعی می‌کند یک آیتم پیدا کند، اگر نبود آن را می‌سازد
    wishlist_item, created = WishList.objects.get_or_create(user=request.user, product=product)

    if created:
        # یعنی محصول در لیست نبود و الان ساخته شد (اضافه شد)
        return JsonResponse({'status': 'added', 'message': 'محصول به لیست علاقه‌مندی‌ها اضافه شد.'})
    else:
        # یعنی محصول از قبل در لیست بود، پس باید حذف شود
        wishlist_item.delete()
        return JsonResponse({'status': 'removed', 'message': 'محصول از لیست علاقه‌مندی‌ها حذف شد.'})


class WishlistPageView(LoginRequiredMixin, ListView):
    model = Product # ما همچنان می‌خواهیم لیستی از "محصولات" را نمایش دهیم
    template_name = 'products/wishlist.html' # تمپلیت جدید ما
    context_object_name = 'wishlist_products' # نام متغیر در این تمپلیت
    paginate_by = 4 # می‌توانید صفحه‌بندی هم داشته باشید

    def get_queryset(self):
        # این متد را بازنویسی می‌کنیم تا فقط محصولاتی را برگرداند
        # که در لیست علاقه‌مندی‌های کاربر فعلی وجود دارند.
        
        # ابتدا لیست ID محصولاتی که کاربر لایک کرده را پیدا می‌کنیم
        user_wishlist_pks = WishList.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        
        # سپس فقط محصولاتی را از مدل Product برمی‌گردانیم که ID آنها در لیست بالا باشد
        queryset = Product.objects.filter(pk__in=user_wishlist_pks)
        
        return queryset

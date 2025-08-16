from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from .models import Product, Category, Comment
from django.shortcuts import get_object_or_404

from .forms import CommentForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products' # نام متغیری که در تمپلیت استفاده می‌شود
    queryset = Product.objects.all()
    paginate_by = 4


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





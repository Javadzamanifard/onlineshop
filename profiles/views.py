from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm



class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        profile_user = self.get_object().user
        # context['product'] = product.objects.filter(author=profile_user).order_by('-created_at').prefetch_related('author__profile')
        return context



@login_required
def profile_update_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل شما با موفقیت بروزرسانی شد!')
            return redirect(request.user.profile.get_absolute_url())
        else:
            messages.error(request, 'لطفا خطاهای زیر را اصلاح کنید.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profiles/profile_form.html', context)


@login_required  # این دکوراتور تضمین می‌کند که فقط کاربران لاگین کرده به این ویو دسترسی دارند
def my_profile_view(request):
    # پروفایل مرتبط با کاربری که در حال حاضر لاگین است را پیدا می‌کنیم
    # استفاده از try-except برای جلوگیری از خطا در صورتی که کاربری پروفایل نداشته باشد
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # اگر پروفایلی برای کاربر وجود نداشت، می‌توانید یکی بسازید یا یک پیام خطا نمایش دهید
        # در اینجا ما فرض می‌کنیم که پروفایل همیشه وجود دارد.
        # اگر کاربر جدید ثبت‌نام می‌کند، باید یک پروفایل هم برایش بسازید (با استفاده از signals)
        profile = None

    context = {
        'profile': profile
    }
    return render(request, 'profiles/profile_detail.html', context)
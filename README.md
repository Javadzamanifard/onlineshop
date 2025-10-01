یک فروشگاه آنلاین کامل و حرفه‌ای ساخته شده با Django

ویژگی‌های پروژه
ماژول‌های اصلی
Accounts: مدیریت کاربران و احراز هویت

Products: مدیریت محصولات و دسته‌بندی‌ها

Cart: سبد خرید و مدیریت آیتم‌ها

Orders: سیستم سفارش‌دهی و پیگیری

Payment: درگاه پرداخت و تراکنش‌ها

Profiles: پروفایل کاربران و اطلاعات شخصی

تکنولوژی‌ها
Backend: Django 4.x/3.x

Database: Mysql

Frontend: HTML, CSS, JavaScript

Template Engine: Django Templates

Static Files: WhiteNoise

Environment: python-decouple

ساختار پروژه
text
onlineshop/
├── accounts/          # مدیریت کاربران
├── products/          # ماژول محصولات
├── cart/             # سبد خرید
├── orders/           # سیستم سفارش
├── payment/          # درگاه پرداخت
├── profiles/         # پروفایل کاربران
├── templates/        # فایل‌های قالب
├── static/           # فایل‌های استاتیک
├── media/            # فایل‌های رسانه‌ای
├── config/           # تنظیمات پروژه
├── requirements.txt  # وابستگی‌های پروژه
└── manage.py         # اسکریپت مدیریت Django
نصب و راه‌اندازی
پیش‌نیازها
Python 3.8+

pip (Python package manager)

مراحل نصب
کلون کردن ریپازیتوری

bash
git clone https://github.com/davazamanifard/onlineshop.git
cd onlineshop
ایجاد محیط مجازی

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate     # Windows
نصب وابستگی‌ها

bash
pip install -r requirements.txt
اجرای migrations

bash
python manage.py migrate
ایجاد کاربر ابری (اختیاری)

bash
python manage.py createsuperuser
اجرای سرور توسعه

bash
python manage.py runserver
پیکربندی
تنظیمات محیطی
فایل env را در روت پروژه ایجاد کنید:

ini
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
تنظیمات پایگاه داده
پروژه از SQLite به صورت پیش‌فرض استفاده می‌کند. برای محیط production می‌توانید از PostgreSQL استفاده کنید.

امکانات کلیدی
سیستم کاربران
ثبت‌نام و ورود کاربران

بازیابی رمز عبور

پروفایل کاربری

سطوح دسترسی مختلف

مدیریت محصولات
دسته‌بندی محصولات

جستجوی پیشرفته

سیستم امتیازدهی و نظرات

مدیریت موجودی

سبد خرید
افزودن/حذف محصولات

به‌روزرسانی تعداد

محاسبه خودکار قیمت

ذخیره سبد خرید

سیستم پرداخت
درگاه پرداخت امن

پیگیری تراکنش‌ها

تاریخچه خرید

استقرار (Deployment)
برای استقرار روی Heroku:
bash
# نصب Heroku CLI
heroku create your-app-name

# تنظیم متغیرهای محیطی
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret

# استقرار
git push heroku main

# اجرای migrations
heroku run python manage.py migrate
برای استقرار روی PythonAnywhere:
آپلود پروژه از طریق گیت

تنظیم virtual environment

پیکربندی فایل WSGI

اجرای migrations

مشارکت در پروژه
فورک (Fork) پروژه

ایجاد شاخه جدید (git checkout -b feature/AmazingFeature)

کامیت تغییرات (git commit -m 'Add some AmazingFeature')

پوش به شاخه (git push origin feature/AmazingFeature)

ایجاد Pull Request

توضیحات فنی
ماژول‌های سفارشی
persiantarisation: ابزارهای فارسی‌سازی

Api: REST API endpoints

gligmore: ماژول‌های کمکی

مدیریت استاتیک و مدیا
فایل‌های استاتیک در پوشه static/

فایل‌های آپلودی کاربران در media/

پیکربندی شده برای سرو‌دهی در محیط production



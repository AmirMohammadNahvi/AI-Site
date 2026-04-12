# FaralYar

نسخه اول FaralYar با Django، رابط فارسی RTL، داشبورد کاربری، چت هوش مصنوعی، پلن‌های اشتراک، وبلاگ و پنل ادمین سفارشی.

## اجرا

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## قابلیت‌های فعلی

- طراحی فارسی و mobile-first
- light/dark mode
- صفحات عمومی: خانه، قیمت‌گذاری، درباره ما، تماس، قوانین، حریم خصوصی، FAQ
- وبلاگ: مقاله، دسته‌بندی، نویسنده، جست‌وجوی ساده
- احراز هویت با ایمیل/رمز و موبایل/OTP
- چت AI با مدل‌های قابل‌تعریف از پنل
- تحلیل متن، تصویر ورودی و فایل ورودی
- پلن‌های مدت‌دار با quota و reset window
- پرداخت زرین‌پال با callback
- داشبورد کاربر و ادمین سفارشی
- Django Admin برای مدیریت عمیق

## نکات

- اگر سرویس OTP تنظیم نشده باشد، در محیط توسعه کد در پیام‌های Django نمایش داده می‌شود.
- برای پرداخت واقعی باید `ZARINPAL_MERCHANT_ID` یا مقدار آن در تنظیمات سایت ثبت شود.
- لوگوهای برند از پوشه `static/branding` بارگذاری می‌شوند و از فایل‌های قرارگرفته در پوشه `logos` کپی شده‌اند.

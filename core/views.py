from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from ai_platform.models import AIModel
from billing.models import Plan
from billing.services import get_active_subscription

from .forms import ContactForm
from .models import FAQItem, SiteSetting, StaticPage


DEFAULT_PAGE_CONTENT = {
    "about": "فارال یار دستیار هوش مصنوعی تیم فارال است؛ یک تجربه فارسی‌محور برای گفتگو با مدل‌های متنوع، مدیریت اشتراک و محتوای آموزشی.",
    "terms": "استفاده از خدمات FaralYar به معنای پذیرش قوانین، حفظ امنیت حساب کاربری و رعایت استفاده مسئولانه از ابزارهای هوش مصنوعی است.",
    "privacy": "FaralYar داده‌های لازم برای ارائه خدمات را نگهداری می‌کند و از اطلاعات کاربران برای اجرای سرویس، مدیریت حساب و امنیت استفاده می‌شود.",
    "faq": "در این بخش می‌توانید سوالات پرتکرار درباره پلن‌ها، محدودیت پیام، روش پرداخت و استفاده از مدل‌ها را ببینید.",
}


def home(request):
    context = {
        "featured_models": AIModel.objects.filter(is_active=True, is_featured=True)[:6],
        "plans": Plan.objects.filter(is_active=True)[:3],
    }
    return render(request, "core/home.html", context)


def _format_amount(value):
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def _clean_feature_items(raw_items):
    seen = set()
    items = []
    for raw_item in raw_items:
        if raw_item is None:
            continue
        text = str(raw_item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        items.append(text)
    return items


def _extract_plan_feature_items(plan):
    features = plan.features or {}
    items = []
    if isinstance(features, list):
        items.extend(features)
    elif isinstance(features, dict):
        for key in ("highlights", "included_items", "items", "features"):
            value = features.get(key)
            if isinstance(value, list):
                items.extend(value)
    return _clean_feature_items(items)


def _plan_role(total_plans, index):
    if total_plans <= 1:
        return "recommended"
    if total_plans == 2:
        return "starter" if index == 0 else "advanced"

    recommended_index = 1 if total_plans <= 3 else total_plans // 2
    if index == 0:
        return "starter"
    if index == total_plans - 1:
        return "advanced"
    if index == recommended_index:
        return "recommended"
    return "growth"


def _role_copy(role):
    copy_map = {
        "starter": {
            "badge": "پلن شروع",
            "eyebrow": "برای شروع آرام",
            "fit_title": "برای کسی که می‌خواهد با هزینه کنترل‌شده وارد استفاده واقعی شود",
            "fit_body": "اگر هنوز در حال سنجیدن ریتم استفاده خود هستید و می‌خواهید بدون فشار وارد تجربه اصلی شوید، این سطح نقطه شروع آرام‌تری است.",
            "value_story": "هزینه و سطح دسترسی را ساده نگه می‌دارد تا انتخاب اول مبهم یا سنگین نشود.",
            "choose_if": "اگر استفاده شما هنوز سبک‌تر، فردی‌تر یا آزمایشی‌تر است.",
            "avoid_if": "اگر از همان ابتدا به ظرفیت بالاتر یا تنوع دسترسی بیشتری نیاز دارید.",
            "access_label": "سطح دسترسی پایه",
            "tone": "starter",
        },
        "growth": {
            "badge": "پلن متعادل",
            "eyebrow": "برای رشد بعد از شروع",
            "fit_title": "برای کسی که از شروع عبور کرده و به ثبات بیشتری نیاز دارد",
            "fit_body": "وقتی استفاده شما منظم‌تر شده اما هنوز به بالاترین سطح دسترسی نیاز ندارید، این پلن نقطه تعادل روشن‌تری ایجاد می‌کند.",
            "value_story": "بین سادگی انتخاب و ظرفیت بیشتر تعادل برقرار می‌کند.",
            "choose_if": "اگر استفاده شما پیوسته شده اما هنوز سنگین‌ترین سناریو نیست.",
            "avoid_if": "اگر انتظار شما از همان ابتدا نزدیک به نیازهای پیشرفته یا تیمی است.",
            "access_label": "سطح دسترسی متعادل",
            "tone": "growth",
        },
        "recommended": {
            "badge": "پیشنهاد برای بیشتر کاربران",
            "eyebrow": "بهترین نقطه تعادل",
            "fit_title": "برای استفاده منظم، شفاف و بدون حدس‌وگمان",
            "fit_body": "اگر می‌خواهید با یک انتخاب مطمئن وارد استفاده روزمره شوید و بین قیمت، دسترسی و ظرفیت تعادل داشته باشید، این پلن معمولاً روشن‌ترین گزینه است.",
            "value_story": "برای بیشتر کاربران، ساده‌ترین پاسخ به این پرسش است که چه چیزی بعد از پرداخت عوض می‌شود.",
            "choose_if": "اگر می‌خواهید بدون ریسک تصمیم اشتباه، روی پلنی متعادل شروع کنید.",
            "avoid_if": "اگر فقط استفاده‌ای بسیار محدود دارید یا از همان ابتدا سطح بالاتری لازم دارید.",
            "access_label": "سطح دسترسی پیشنهادی",
            "tone": "recommended",
        },
        "advanced": {
            "badge": "پلن پیشرفته",
            "eyebrow": "برای استفاده سنگین‌تر",
            "fit_title": "برای کسی که به ظرفیت و دسترسی گسترده‌تری نیاز دارد",
            "fit_body": "اگر ریتم استفاده شما جدی‌تر شده یا برای کار حرفه‌ای‌تر به سقف بالاتر و دسترسی وسیع‌تری نیاز دارید، این پلن منطقی‌تر است.",
            "value_story": "برای زمانی طراحی شده که محدودیت پلن‌های پایین‌تر زودتر به چشم می‌آید.",
            "choose_if": "اگر از محصول به‌صورت پیوسته‌تر استفاده می‌کنید یا رشد بعدی برایتان مهم است.",
            "avoid_if": "اگر هنوز در مرحله شروع هستید و نمی‌خواهید از ابتدا پلن سنگین‌تری بگیرید.",
            "access_label": "سطح دسترسی پیشرفته",
            "tone": "advanced",
        },
    }
    return copy_map[role]


def _build_plan_cards(request, plans):
    current_subscription = get_active_subscription(request.user) if request.user.is_authenticated else None
    current_plan_slug = current_subscription.plan.slug if current_subscription else None
    total_plans = len(plans)
    plan_cards = []

    for index, plan in enumerate(plans):
        role = _plan_role(total_plans, index)
        role_copy = _role_copy(role)
        is_recommended = role == "recommended" or (total_plans == 2 and index == total_plans - 1)
        model_count = plan.allowed_models.count()
        feature_items = _extract_plan_feature_items(plan)
        change_points = [
            f"این سطح برای {plan.duration_days} روز روی حساب شما فعال می‌شود.",
            f"سقف مصرف هر بازه روی {plan.token_limit_per_window} و بازنشانی روی هر {plan.reset_interval_hours} ساعت تنظیم می‌شود.",
            (
                f"برای این پلن {model_count} مدل مجاز تعریف شده است."
                if model_count
                else "فهرست مدل‌های مجاز این پلن هنوز به‌صورت روشن ثبت نشده است."
            ),
        ]
        included_items = feature_items[:3] or [
            role_copy["value_story"],
            f"{plan.duration_days} روز اعتبار با بازه‌های {plan.reset_interval_hours} ساعته.",
            (
                f"دسترسی تعریف‌شده به {model_count} مدل مجاز."
                if model_count
                else "سطح دسترسی این پلن جداگانه تعریف می‌شود."
            ),
        ]
        limit_points = [
            f"این پلن همچنان سقف {plan.token_limit_per_window} برای هر بازه دارد و بعد از آن باید منتظر بازنشانی بعدی بمانید.",
            f"اعتبار خرید بعد از {plan.duration_days} روز تمام می‌شود و برای ادامه، سفارش تازه لازم است.",
            "سیاست‌های دسترسی خارج از خود پلن فقط با همین خرید به‌تنهایی تغییر نمی‌کنند.",
        ]

        if current_plan_slug == plan.slug:
            cta_url = reverse("ai_platform:billing")
            cta_label = "مرور وضعیت پلن"
            secondary_cta_url = "#pricing-compare"
            secondary_cta_label = "مقایسه با گزینه‌های دیگر"
            state_note = "همین حالا روی حساب شما فعال است."
        elif request.user.is_authenticated:
            cta_url = reverse("billing:checkout", kwargs={"slug": plan.slug})
            cta_label = "انتخاب این پلن" if is_recommended else "ادامه با این پلن"
            secondary_cta_url = "#pricing-compare"
            secondary_cta_label = "اول مقایسه جزئیات"
            state_note = "پس از پرداخت موفق، همین سطح برای حساب شما فعال می‌شود."
        else:
            cta_url = reverse("accounts:signup")
            cta_label = "ساخت حساب و ادامه"
            secondary_cta_url = reverse("accounts:login")
            secondary_cta_label = "حساب دارید؟ ورود"
            state_note = "برای ادامه خرید باید وارد حساب خود شوید."

        plan_cards.append(
            {
                "id": f"plan-{plan.slug}",
                "slug": plan.slug,
                "name": plan.name,
                "eyebrow": role_copy["eyebrow"],
                "badge": role_copy["badge"],
                "fit_title": role_copy["fit_title"],
                "fit_statement": plan.description or role_copy["fit_body"],
                "value_summary": role_copy["value_story"],
                "choose_if": role_copy["choose_if"],
                "avoid_if": role_copy["avoid_if"],
                "access_label": role_copy["access_label"],
                "state_note": state_note,
                "price": _format_amount(plan.price),
                "currency_label": "تومان",
                "duration": f"{plan.duration_days} روز اعتبار",
                "price_note": f"بازنشانی مصرف هر {plan.reset_interval_hours} ساعت انجام می‌شود.",
                "included_items": included_items,
                "change_points": change_points,
                "limit_points": limit_points,
                "meta_items": [
                    {"label": "مدت خرید", "value": f"{plan.duration_days} روز"},
                    {"label": "سقف هر بازه", "value": str(plan.token_limit_per_window)},
                    {"label": "بازنشانی", "value": f"هر {plan.reset_interval_hours} ساعت"},
                    {"label": "مدل‌های مجاز", "value": str(model_count) if model_count else "نامشخص"},
                ],
                "footnote": "اگر نیاز شما عوض شود، مسیر ارتقا یا بازگشت به مقایسه از همین صفحه روشن می‌ماند.",
                "cta_url": cta_url,
                "cta_label": cta_label,
                "secondary_cta_url": secondary_cta_url,
                "secondary_cta_label": secondary_cta_label,
                "is_current": current_plan_slug == plan.slug,
                "is_recommended": is_recommended,
                "role": role,
                "tone": role_copy["tone"],
            }
        )

    return plan_cards, current_plan_slug


def _build_audience_rows(plan_cards):
    rows = []
    for plan in plan_cards:
        rows.append(
            {
                "plan_name": plan["name"],
                "badge": plan["badge"],
                "title": plan["fit_title"],
                "body": plan["fit_statement"],
                "good_for": plan["choose_if"],
                "not_for": plan["avoid_if"],
                "anchor": f"#{plan['id']}",
                "tone": plan["tone"],
            }
        )
    return rows


def _build_comparison_sections(plan_cards):
    if not plan_cards:
        return []

    shared_limit_note = "این بخش برای تصمیم‌گیری است، نه تعریف قانون جدید. وضعیت نهایی حساب بعد از خرید موفق و بر اساس پلن انتخابی اعمال می‌شود."
    return [
        {
            "title": "کدام پلن برای چه ریتمی مناسب‌تر است؟",
            "badge": "راهنمای انتخاب",
            "summary": "اگر اول می‌خواهید بدانید هر پلن برای چه سبک استفاده‌ای ساخته شده، این بخش سریع‌ترین تصویر را می‌دهد.",
            "open_by_default": True,
            "items": [
                {
                    "label": "نوع استفاده",
                    "description": "به‌جای مقایسه فنی، ببینید هر پلن برای چه نوع تصمیمی مناسب‌تر است.",
                    "plan_points": [{"plan_name": plan["name"], "value": plan["fit_title"]} for plan in plan_cards],
                },
                {
                    "label": "چرخه برنامه‌ریزی",
                    "description": "این خرید را برای چه بازه‌ای برنامه‌ریزی می‌کنید.",
                    "plan_points": [{"plan_name": plan["name"], "value": plan["duration"]} for plan in plan_cards],
                },
                {
                    "label": "فشار مصرف",
                    "description": "اگر ریتم استفاده شما بیشتر یا کمتر است، این بخش تفاوت را شفاف می‌کند.",
                    "plan_points": [
                        {
                            "plan_name": plan["name"],
                            "value": f"سقف هر بازه {plan['meta_items'][1]['value']} با بازنشانی {plan['meta_items'][2]['value']}",
                        }
                        for plan in plan_cards
                    ],
                },
            ],
            "note": shared_limit_note,
        },
        {
            "title": "بعد از پرداخت چه چیزی تغییر می‌کند؟",
            "badge": "تغییرات بعد از خرید",
            "summary": "این بخش کمک می‌کند بدانید با پرداخت موفق، چه چیز فوراً روشن و فعال می‌شود.",
            "items": [
                {
                    "label": "سطح فعال روی حساب",
                    "description": "این همان تغییری است که خرید واقعاً برای حساب شما ایجاد می‌کند.",
                    "plan_points": [{"plan_name": plan["name"], "value": plan["change_points"][0]} for plan in plan_cards],
                },
                {
                    "label": "ظرفیت و بازنشانی",
                    "description": "تفاوت در سقف هر بازه و ریتم بازنشانی از همین‌جا مشخص است.",
                    "plan_points": [{"plan_name": plan["name"], "value": plan["change_points"][1]} for plan in plan_cards],
                },
                {
                    "label": "تنوع دسترسی تعریف‌شده",
                    "description": "خرید پلن، فقط دسترسی‌های تعریف‌شده برای همان پلن را اعمال می‌کند.",
                    "plan_points": [{"plan_name": plan["name"], "value": plan["change_points"][2]} for plan in plan_cards],
                },
            ],
            "note": "هیچ تغییری قبل از تایید موفق پرداخت روی حساب شما اعمال نمی‌شود.",
        },
        {
            "title": "چه چیزهایی همچنان محدود می‌ماند؟",
            "badge": "صادقانه درباره محدودیت‌ها",
            "summary": "این قسمت برای جلوگیری از انتخاب اشتباه است: هر پلن همچنان سقف و مرز خودش را دارد.",
            "items": [
                {
                    "label": "سقف مصرف هر بازه",
                    "description": "هیچ پلنی بدون سقف نیست؛ فقط اندازه و ریتم سقف فرق می‌کند.",
                    "plan_points": [{"plan_name": plan["name"], "value": plan["limit_points"][0]} for plan in plan_cards],
                },
                {
                    "label": "پایان اعتبار خرید",
                    "description": "هر خرید یک بازه روشن دارد و برای ادامه باید وضعیت بعدی مشخص شود.",
                    "plan_points": [{"plan_name": plan["name"], "value": plan["limit_points"][1]} for plan in plan_cards],
                },
                {
                    "label": "موارد خارج از خود پلن",
                    "description": "این صفحه قول تغییرِ چیزهایی را نمی‌دهد که بیرون از تعریف پلن هستند.",
                    "plan_points": [{"plan_name": plan["name"], "value": plan["limit_points"][2]} for plan in plan_cards],
                },
            ],
            "note": "اگر درباره دسترسی دقیق یا وضعیت فعلی حساب سؤال دارید، مرجع نهایی بعد از ورود صفحه اشتراک و پرداخت است.",
        },
    ]


def _build_pricing_faq_items():
    faq_queryset = FAQItem.objects.filter(is_active=True)
    if faq_queryset.exists():
        return [{"question": item.question, "answer": item.answer, "note": ""} for item in faq_queryset[:6]]

    return [
        {
            "question": "بعد از پرداخت موفق چه زمانی پلن فعال می‌شود؟",
            "answer": "بعد از تایید موفق پرداخت، سفارش ثبت می‌شود و همان پلن برای حساب شما فعال خواهد شد. قبل از تایید نهایی، سطح دسترسی حساب تغییر نمی‌کند.",
            "note": "مرور نهایی و نتیجه پرداخت در مسیر خرید و وضعیت سفارش دیده می‌شود.",
        },
        {
            "question": "اگر بعداً به پلن دیگری نیاز داشته باشم چه می‌شود؟",
            "answer": "صفحه قیمت‌گذاری برای این طراحی شده که مسیر ارتقا یا انتخاب بعدی روشن بماند. اگر نیاز شما تغییر کند، می‌توانید دوباره پلن مناسب‌تر را بررسی و انتخاب کنید.",
            "note": "این صفحه قرار نیست شما را به یک انتخاب غیرقابل بازگشت هل دهد.",
        },
        {
            "question": "آیا با خرید پلن همه محدودیت‌ها برداشته می‌شود؟",
            "answer": "خیر. هر پلن همچنان مدت اعتبار، سقف مصرف هر بازه و محدوده دسترسی خودش را دارد. این صفحه عمداً این محدودیت‌ها را پنهان نمی‌کند.",
            "note": "",
        },
        {
            "question": "اگر قبل از پرداخت مطمئن نباشم، باید چه کار کنم؟",
            "answer": "از پلنی شروع کنید که با ریتم فعلی استفاده شما هماهنگ‌تر است، نه پلنی که فقط بزرگ‌تر به نظر می‌رسد. اگر هنوز ابهام داشتید، بهتر است قبل از خرید با تیم پشتیبانی تماس بگیرید.",
            "note": "",
        },
    ]


def pricing(request):
    active_plans = list(Plan.objects.filter(is_active=True).prefetch_related("allowed_models"))
    plan_cards, current_plan_slug = _build_plan_cards(request, active_plans)
    recommended_plan = next((plan for plan in plan_cards if plan["is_recommended"]), None)

    if request.user.is_authenticated and current_plan_slug:
        hero_primary_url = reverse("ai_platform:billing")
        hero_primary_label = "مرور وضعیت پلن فعلی"
    else:
        hero_primary_url = "#pricing-plans"
        hero_primary_label = "مرور پلن‌ها"

    trust_support_url = reverse("core:contact")
    trust_support_label = "تماس با تیم"
    site_settings = SiteSetting.get_solo()
    if site_settings.payment_guide_url:
        trust_support_url = site_settings.payment_guide_url
        trust_support_label = "راهنمای پرداخت"

    return render(
        request,
        "public/pricing.html",
        {
            "plans": plan_cards,
            "pricing_badges": [
                "قیمت‌گذاری آرام و شفاف",
                "انتخاب بر اساس نوع استفاده",
                "صادقانه درباره محدودیت‌ها",
            ],
            "pricing_heading": "پلنی را انتخاب کنید که با ریتم واقعی کار شما هماهنگ باشد.",
            "pricing_subheading": "این صفحه برای فشار آوردن به خرید ساخته نشده است. هدفش این است که خیلی سریع بفهمید هر پلن برای چه نوع استفاده‌ای مناسب است، بعد از پرداخت چه تغییری ایجاد می‌شود و چه چیزهایی همچنان محدود می‌ماند.",
            "pricing_highlights": [
                {
                    "title": "اول انتخاب، بعد خرید",
                    "body": "پیش از هر CTA، تفاوت پلن‌ها از زاویه کاربرد، سطح دسترسی و محدودیت‌ها توضیح داده می‌شود.",
                },
                {
                    "title": "تفاوت‌ها در زبان محصول",
                    "body": "به‌جای جدول شلوغ، پلن‌ها با سناریوی استفاده، ظرفیت هر بازه و افق زمانی معرفی می‌شوند.",
                },
                {
                    "title": "مسیر خرید قابل پیش‌بینی",
                    "body": "مرور خرید، پرداخت و فعال‌سازی هرکدام جای مشخص خود را دارند و وعده مبهمی داده نمی‌شود.",
                },
            ],
            "primary_cta_url": hero_primary_url,
            "primary_cta_label": hero_primary_label,
            "secondary_cta_url": "#pricing-compare",
            "secondary_cta_label": "راهنمای مقایسه",
            "hero_aside_badge": "سه پرسش اصلی",
            "hero_aside_title": "برای انتخاب درست فقط این سه چیز را با خودتان روشن کنید.",
            "hero_aside_points": [
                {
                    "title": "چقدر منظم استفاده می‌کنید؟",
                    "body": "اگر هنوز در حال شروع هستید، پلن سبک‌تر تصمیم کم‌فشارتری است. اگر استفاده شما منظم شده، پلن متعادل یا پیشرفته معنا پیدا می‌کند.",
                },
                {
                    "title": "بعد از خرید دقیقاً چه می‌خواهید عوض شود؟",
                    "body": "این صفحه روشن می‌گوید خرید هر پلن چه سطحی از دسترسی و چه ظرفیتی را فعال می‌کند، نه بیشتر از آن.",
                },
                {
                    "title": "با چه محدودیتی مشکلی ندارید؟",
                    "body": "هر پلن همچنان سقف هر بازه، مدت اعتبار و محدوده دسترسی خودش را دارد. اگر این مرزها مهم‌اند، مقایسه پایین صفحه را ببینید.",
                },
            ],
            "plans_section_title": "سه مسیر روشن برای سه نوع تصمیم",
            "plans_section_body": "پلن‌ها باید حس متفاوتی داشته باشند، نه این‌که فقط چند عدد روی کارت عوض شود. برای همین هر کارت هم درباره تناسب استفاده توضیح می‌دهد، هم درباره چیزی که بعد از پرداخت واقعاً تغییر می‌کند.",
            "plans_section_note": "اگر وارد حساب خود شده باشید، پلن فعلی‌تان هم روی همین صفحه مشخص می‌شود.",
            "audience_rows": _build_audience_rows(plan_cards),
            "comparison_heading": "مقایسه‌ای که به تصمیم کمک می‌کند، نه این‌که شما را خسته کند",
            "comparison_subheading": "هر بخش فقط یک سؤال اصلی را جواب می‌دهد: این پلن برای چه کسی است، بعد از خرید چه فرق می‌کند، و چه محدودیت‌هایی همچنان باقی می‌ماند.",
            "comparison_sections": _build_comparison_sections(plan_cards),
            "trust_badge": "اعتماد و پرداخت",
            "trust_title": "پرداخت باید مطمئن، مرحله‌به‌مرحله و بدون ابهام باشد.",
            "trust_body": "این صفحه فقط قول چیزهایی را می‌دهد که واقعاً در مسیر خرید و فعال‌سازی اتفاق می‌افتد. نه تغییری قبل از پرداخت موفق اعمال می‌شود، نه محدودیت‌های بیرون از تعریف پلن به‌صورت مبهم فروخته می‌شوند.",
            "payment_steps": [
                {
                    "step": "1",
                    "title": "مرور نهایی پلن",
                    "body": "قبل از ورود به درگاه، خلاصه روشن همان پلنی را که انتخاب کرده‌اید می‌بینید تا تصمیم شما از روی حدس نباشد.",
                },
                {
                    "step": "2",
                    "title": "پرداخت و ثبت وضعیت سفارش",
                    "body": "پس از انتقال به درگاه، نتیجه نهایی در مسیر وضعیت سفارش ثبت می‌شود تا مرجع روشنی برای پرداخت داشته باشید.",
                },
                {
                    "step": "3",
                    "title": "فعال‌سازی بعد از تایید موفق",
                    "body": "پلن فقط بعد از تایید موفق برای حساب شما فعال می‌شود و همان‌جا اثر خرید روی دسترسی و ظرفیت مشخص خواهد بود.",
                },
            ],
            "trust_items": [
                {
                    "title": "بدون تغییر پنهان روی حساب",
                    "body": "اگر پرداخت کامل نشود، پلن جدید روی حساب شما فعال نمی‌شود و وضعیت قبلی ناگهان عوض نخواهد شد.",
                },
                {
                    "title": "تاریخچه شما با خرید حذف نمی‌شود",
                    "body": "هدف خرید، تغییر سطح اشتراک و ظرفیت تعریف‌شده است؛ نه پاک‌کردن گفتگوها یا ریست‌کردن مسیر کاری قبلی شما.",
                },
                {
                    "title": "محدودیت‌ها همچنان شفاف می‌مانند",
                    "body": "هر پلن هنوز مدت اعتبار، سقف هر بازه و محدوده دسترسی خودش را دارد و این صفحه آن‌ها را پنهان نمی‌کند.",
                },
                {
                    "title": "پشتیبانی پیش از خرید در دسترس است",
                    "body": site_settings.payment_guide_text or "اگر قبل از پرداخت نیاز به اطمینان بیشتری داشته باشید، مسیر راهنما یا تماس مستقیم در دسترس است.",
                },
            ],
            "trust_support_card": {
                "title": "اگر هنوز درباره پرداخت یا تناسب پلن مطمئن نیستید",
                "body": "قبل از رفتن به مسیر خرید، می‌توانید راهنمای پرداخت را ببینید یا سؤال خود را با تیم مطرح کنید تا تصمیم‌گیری آرام‌تری داشته باشید.",
                "cta_url": trust_support_url,
                "cta_label": trust_support_label,
            },
            "faq_intro_badge": "پرسش‌های رایج",
            "faq_intro_title": "سوال‌هایی که معمولاً قبل از انتخاب نهایی پرسیده می‌شوند",
            "faq_intro_body": "این پاسخ‌ها کوتاه و واقع‌گرایانه نوشته شده‌اند تا تردیدهای متداول را بدون زبان فروش برطرف کنند.",
            "faq_support_note": {
                "title": "هنوز مورد شما بین این سوال‌ها نیست؟",
                "body": "اگر وضعیت فعلی حساب یا نیاز شما خاص‌تر است، بهتر است قبل از خرید آن را مستقیم با تیم بررسی کنید.",
                "cta_url": reverse("core:contact"),
                "cta_label": "طرح سوال",
            },
            "faq_items": _build_pricing_faq_items(),
            "final_cta_title": "اگر هنوز بین دو پلن مردد هستید، از گزینه‌ای شروع کنید که امروز واقعاً به آن نیاز دارید.",
            "final_cta_body": (
                f"برای بیشتر کاربران، {recommended_plan['name']} نقطه شروع متعادل‌تری است."
                if recommended_plan
                else "بهترین تصمیم، انتخاب پلنی است که با ریتم فعلی استفاده شما سازگار باشد؛ نه پلنی که فقط بزرگ‌تر به نظر می‌رسد."
            ),
            "final_cta_primary_url": f"#{recommended_plan['id']}" if recommended_plan else "#pricing-plans",
            "final_cta_primary_label": (
                f"مرور دوباره {recommended_plan['name']}" if recommended_plan else "بازگشت به پلن‌ها"
            ),
            "final_cta_secondary_url": "#pricing-faq",
            "final_cta_secondary_label": "مرور سوالات متداول",
        },
    )


def static_page(request, page_key):
    page, _ = StaticPage.objects.get_or_create(
        page_key=page_key,
        defaults={
            "title": dict(StaticPage.PAGE_CHOICES).get(page_key, page_key),
            "body": DEFAULT_PAGE_CONTENT.get(page_key, ""),
        },
    )
    if page_key == StaticPage.FAQ:
        return render(request, "core/faq.html", {"page": page, "faqs": FAQItem.objects.filter(is_active=True)})
    return render(request, "core/static_page.html", {"page": page})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما ثبت شد. به زودی با شما تماس می‌گیریم.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


@require_POST
def set_theme(request):
    theme = request.POST.get("theme", "system")
    if theme in {"light", "dark", "system"}:
        request.session["theme"] = theme
        if request.user.is_authenticated:
            request.user.theme_preference = theme
            request.user.save(update_fields=["theme_preference", "updated_at"])
    return redirect(request.META.get("HTTP_REFERER", "core:home"))

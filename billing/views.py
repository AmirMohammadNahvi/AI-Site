from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ai_platform.app_ui import (
    build_app_shell_context,
    build_checkout_plan_context,
    build_order_status_context,
)
from billing.services import get_active_subscription

from .models import Plan, PurchaseOrder
from .services import BillingError, ZarinpalService, activate_plan_for_order


def _start_checkout(request, plan):
    order = PurchaseOrder.objects.create(
        user=request.user,
        plan=plan,
        amount=plan.price,
        description=f"خرید پلن {plan.name}",
    )
    try:
        payment_url = ZarinpalService.create_payment_request(request, order)
        return redirect(payment_url)
    except Exception as exc:
        order.status = PurchaseOrder.FAILED
        order.save(update_fields=["status", "updated_at"])
        messages.error(request, f"شروع پرداخت ممکن نشد: {exc}")
        return redirect("billing:order_status", order_id=order.id)


@login_required
def checkout(request, slug):
    plan = get_object_or_404(Plan.objects.prefetch_related("allowed_models"), slug=slug, is_active=True)
    if request.method == "POST" or request.GET.get("direct") == "1":
        return _start_checkout(request, plan)

    subscription = get_active_subscription(request.user)
    context = build_app_shell_context(
        request,
        active_nav="billing",
        page_title="مرور خرید",
        page_description="مرور نهایی سفارش قبل از انتقال به پرداخت.",
        page_eyebrow="خرید پلن",
    )
    context.update(build_checkout_plan_context(plan, current_plan_label=subscription.plan.name if subscription else None))
    context["checkout_primary_cta_url"] = f"{request.path}?direct=1"
    context["checkout_primary_cta_label"] = "ادامه به پرداخت"
    context["checkout_secondary_cta_url"] = reverse("ai_platform:billing")
    return render(request, "app/billing/checkout_review.html", context)


@login_required
def order_status(request, order_id):
    order = get_object_or_404(
        PurchaseOrder.objects.select_related("plan").prefetch_related("transactions"),
        id=order_id,
        user=request.user,
    )
    context = build_app_shell_context(
        request,
        active_nav="billing",
        page_title="وضعیت سفارش",
        page_description="مرجع نهایی وضعیت همین سفارش و پرداخت.",
        page_eyebrow="وضعیت سفارش",
    )
    context.update(build_order_status_context(order))
    return render(request, "app/billing/order_status.html", context)


@login_required
def verify(request):
    authority = request.GET.get("Authority", "")
    status = request.GET.get("Status", "")
    order = PurchaseOrder.objects.filter(user=request.user, authority=authority).order_by("-created_at").first()
    if not order:
        messages.error(request, "سفارش معتبر پیدا نشد.")
        return redirect("ai_platform:billing")
    if status != "OK":
        order.status = PurchaseOrder.CANCELED
        order.save(update_fields=["status", "updated_at"])
        messages.error(request, "پرداخت توسط کاربر لغو شد.")
        return redirect("billing:order_status", order_id=order.id)
    try:
        ref_id = ZarinpalService.verify_payment(order, authority)
        activate_plan_for_order(order)
        messages.success(request, f"پرداخت شما با موفقیت انجام شد. کد رهگیری: {ref_id}")
    except BillingError as exc:
        order.status = PurchaseOrder.FAILED
        order.save(update_fields=["status", "updated_at"])
        messages.error(request, str(exc))
    return redirect("billing:order_status", order_id=order.id)

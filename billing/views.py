from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Plan, PurchaseOrder
from .services import BillingError, ZarinpalService, activate_plan_for_order


@login_required
def checkout(request, slug):
    plan = get_object_or_404(Plan, slug=slug, is_active=True)
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
        return redirect("core:pricing")


@login_required
def verify(request):
    authority = request.GET.get("Authority", "")
    status = request.GET.get("Status", "")
    order = PurchaseOrder.objects.filter(user=request.user, authority=authority).order_by("-created_at").first()
    if not order:
        messages.error(request, "سفارش معتبر پیدا نشد.")
        return redirect("dashboard:billing")
    if status != "OK":
        order.status = PurchaseOrder.CANCELED
        order.save(update_fields=["status", "updated_at"])
        messages.error(request, "پرداخت توسط کاربر لغو شد.")
        return redirect("dashboard:billing")
    try:
        ref_id = ZarinpalService.verify_payment(order, authority)
        activate_plan_for_order(order)
        messages.success(request, f"پرداخت شما با موفقیت انجام شد. کد رهگیری: {ref_id}")
    except BillingError as exc:
        order.status = PurchaseOrder.FAILED
        order.save(update_fields=["status", "updated_at"])
        messages.error(request, str(exc))
    return redirect("dashboard:billing")

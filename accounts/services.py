import logging

from django.conf import settings
from django.core.mail import send_mail

from accounts.models import OTPRequest
from core.models import SiteSetting


logger = logging.getLogger(__name__)


class OTPService:
    @staticmethod
    def is_provider_configured():
        settings_obj = SiteSetting.get_solo()
        return bool(settings_obj.otp_provider_name or settings.OTP_PROVIDER_NAME)

    @classmethod
    def send_code(cls, mobile):
        otp_request, code = OTPRequest.create_for_mobile(mobile)
        provider_name = SiteSetting.get_solo().otp_provider_name or settings.OTP_PROVIDER_NAME
        if provider_name:
            logger.info("OTP sent via %s to %s: %s", provider_name, mobile, code)
        else:
            logger.info("OTP fallback for %s: %s", mobile, code)
        return otp_request, code

    @staticmethod
    def send_email_welcome(user):
        if user.email:
            send_mail(
                subject="به FaralYar خوش آمدید",
                message=f"{user.full_name} عزیز، حساب کاربری شما در FaralYar فعال شد.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

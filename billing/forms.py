from django import forms

from .models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = [
            "name",
            "slug",
            "description",
            "price",
            "duration_days",
            "token_limit_per_window",
            "reset_interval_hours",
            "features",
            "display_order",
            "is_active",
            "allowed_models",
        ]

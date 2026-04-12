from django import forms
from django.contrib.auth import authenticate

from .models import User


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["full_name", "email", "mobile"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            self.add_error("password2", "تکرار رمز عبور مطابقت ندارد.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    identifier = forms.CharField(label="ایمیل یا موبایل")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        identifier = cleaned.get("identifier")
        password = cleaned.get("password")
        user = authenticate(self.request, username=identifier, password=password)
        if not user:
            raise forms.ValidationError("اطلاعات ورود درست نیست.")
        self.user = user
        return cleaned


class OTPRequestForm(forms.Form):
    mobile = forms.CharField(label="شماره موبایل")


class OTPVerifyForm(forms.Form):
    mobile = forms.CharField(widget=forms.HiddenInput)
    code = forms.CharField(label="کد تایید")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "mobile",
            "theme_preference",
            "persona_choice",
            "preferred_name",
            "job_title",
            "interests",
            "custom_instructions",
            "memory_enabled",
        ]


class PersonalizationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "persona_choice",
            "custom_instructions",
            "preferred_name",
            "job_title",
            "interests",
            "memory_enabled",
        ]
        labels = {
            "persona_choice": "انتخاب شخصیت",
            "custom_instructions": "دستورات",
            "preferred_name": "فارال یار شما را چه صدا کند",
            "job_title": "شغل شما",
            "interests": "علایق، ارزش‌ها و سلیقه‌ها که فارال یار در نظر بگیرد",
            "memory_enabled": "حافظه (آزمایشی)",
        }
        widgets = {
            "custom_instructions": forms.Textarea(attrs={"rows": 4}),
            "interests": forms.Textarea(attrs={"rows": 4}),
        }

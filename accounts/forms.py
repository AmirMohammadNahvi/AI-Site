from django import forms
from django.contrib.auth import authenticate

from .models import User


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["full_name", "email", "mobile"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {
                "placeholder": "نام و نام خانوادگی",
                "autocomplete": "name",
                "autofocus": True,
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "dir": "ltr",
                "inputmode": "email",
            }
        )
        self.fields["mobile"].widget.attrs.update(
            {
                "placeholder": "0912 000 0000",
                "autocomplete": "tel",
                "dir": "ltr",
                "inputmode": "tel",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "رمز عبور مطمئن",
                "autocomplete": "new-password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "تکرار رمز عبور",
                "autocomplete": "new-password",
            }
        )

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
        self.fields["identifier"].widget.attrs.update(
            {
                "placeholder": "ایمیل یا شماره موبایل",
                "autocomplete": "username",
                "autofocus": True,
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "رمز عبور",
                "autocomplete": "current-password",
            }
        )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mobile"].widget.attrs.update(
            {
                "placeholder": "0912 000 0000",
                "autocomplete": "tel",
                "dir": "ltr",
                "inputmode": "tel",
                "autofocus": True,
            }
        )


class OTPVerifyForm(forms.Form):
    mobile = forms.CharField(widget=forms.HiddenInput)
    code = forms.CharField(label="کد تایید")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].widget.attrs.update(
            {
                "placeholder": "کد تایید را وارد کنید",
                "autocomplete": "one-time-code",
                "dir": "ltr",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "autofocus": True,
            }
        )


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
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "نام و نام خانوادگی", "autocomplete": "name"}),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                    "dir": "ltr",
                    "inputmode": "email",
                }
            ),
            "mobile": forms.TextInput(
                attrs={
                    "placeholder": "0912 000 0000",
                    "autocomplete": "tel",
                    "dir": "ltr",
                    "inputmode": "tel",
                }
            ),
            "preferred_name": forms.TextInput(attrs={"placeholder": "مثلاً امیر"}),
            "job_title": forms.TextInput(attrs={"placeholder": "مثلاً مدیر محصول"}),
            "interests": forms.Textarea(attrs={"rows": 4, "placeholder": "علایق، سبک کار و چیزهایی که بهتر است در نظر گرفته شوند"}),
            "custom_instructions": forms.Textarea(
                attrs={"rows": 4, "placeholder": "ترجیح لحن، میزان اختصار، یا هر پیش فرض پایداری که می خواهید حفظ شود"}
            ),
        }


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
            "interests": "علایق، ارزش ها و سلیقه ها که فارال یار در نظر بگیرد",
            "memory_enabled": "حافظه (آزمایشی)",
        }
        widgets = {
            "custom_instructions": forms.Textarea(attrs={"rows": 4}),
            "interests": forms.Textarea(attrs={"rows": 4}),
        }

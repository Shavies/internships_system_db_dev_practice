from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import User, Role, University


class RegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ("STUDENT", "STUDENT"),
        ("OWNER", "OWNER"),
    ]

    role_choice = forms.ChoiceField(choices=ROLE_CHOICES)
    university_name = forms.CharField(max_length=100, required=False)

    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ["phone_number", "email", "fname", "lname"]

    def clean(self):
        cleaned = super().clean()

        role = cleaned.get("role_choice")
        uni_name = (cleaned.get("university_name") or "").strip()

        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 != p2:
            raise forms.ValidationError("รหัสผ่านไม่ตรงกัน")
        if p1:
            validate_password(p1)

        # บังคับ university เฉพาะ STUDENT
        if role == "STUDENT" and not uni_name:
            self.add_error("university_name", "กรุณากรอกชื่อมหาวิทยาลัยสำหรับ STUDENT")

        # ถ้า OWNER ให้ล้างค่า university_name
        if role == "OWNER":
            cleaned["university_name"] = ""

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)

        # set password (hash)
        user.set_password(self.cleaned_data["password1"])

        role_name = self.cleaned_data["role_choice"]
        role_obj, _ = Role.objects.get_or_create(name=role_name)
        user.role = role_obj

        if role_name == "OWNER":
            user.is_staff = True
        else:
            user.is_staff = False
        
        # สร้าง University เฉพาะ STUDENT
        uni_name = (self.cleaned_data.get("university_name") or "").strip()
        if role_name == "STUDENT" and uni_name:
            uni_obj, _ = University.objects.get_or_create(name=uni_name)
            user.university = uni_obj
        else:
            user.university = None

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        phone = cleaned.get("phone_number", "").strip()
        password = cleaned.get("password")

        user = authenticate(phone_number=phone, password=password)
        if not user:
            raise forms.ValidationError("เบอร์โทรหรือรหัสผ่านไม่ถูกต้อง")

        cleaned["user"] = user
        return cleaned

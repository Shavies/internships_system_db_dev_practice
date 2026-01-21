from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import User, Role, University, Department, Staff, Student, Major

class BaseRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ["phone_number", "email", "fname", "lname"]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 != p2:
            raise forms.ValidationError("รหัสผ่านไม่ตรงกัน")
        if p1:
            validate_password(p1)
        return cleaned

    def set_user_password(self, user):
        user.set_password(self.cleaned_data["password1"])
        return user


class StudentRegisterForm(BaseRegisterForm):
    university_name = forms.CharField(max_length=100)
    major_name = forms.CharField(max_length=255, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        self.set_user_password(user)

        role_obj, _ = Role.objects.get_or_create(name="STUDENT")
        user.role = role_obj
        user.is_staff = False

        if commit:
            user.save()

        uni, _ = University.objects.get_or_create(name=self.cleaned_data["university_name"].strip())
        major = None
        if self.cleaned_data.get("major_name"):
            major, _ = Major.objects.get_or_create(name=self.cleaned_data["major_name"].strip())

        Student.objects.create(
            user=user,
            university=uni,
            major=major,
            hours=0,
        )
        return user


class OwnerRegisterForm(BaseRegisterForm):
    employee_id = forms.CharField(max_length=50)
    department_id = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        self.set_user_password(user)

        role_obj, _ = Role.objects.get_or_create(name="OWNER")
        user.role = role_obj
        user.is_staff = True  # OWNER เข้า admin ได้

        user.department = self.cleaned_data.get("department_id")

        if commit:
            user.save()

        Staff.objects.create(
            user=user,
            employee_id=self.cleaned_data["employee_id"].strip()
        )
        return user

class StudentLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        phone = cleaned.get("phone_number")
        pw = cleaned.get("password")

        user = authenticate(phone_number=phone, password=pw)
        if user is None:
            raise forms.ValidationError("เบอร์โทรหรือรหัสผ่านไม่ถูกต้อง")
        cleaned["user"] = user
        return cleaned


class OwnerLoginForm(forms.Form):
    employee_id = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        emp = cleaned.get("employee_id")
        pw = cleaned.get("password")

        user = authenticate(employee_id=emp, password=pw)
        if user is None:
            raise forms.ValidationError("employee_id หรือรหัสผ่านไม่ถูกต้อง")
        cleaned["user"] = user
        return cleaned

# class LoginForm(forms.Form):
#     phone_number = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         cleaned = super().clean()
#         phone = cleaned.get("phone_number", "").strip()
#         password = cleaned.get("password")

#         user = authenticate(phone_number=phone, password=password)
#         if not user:
#             raise forms.ValidationError("เบอร์โทรหรือรหัสผ่านไม่ถูกต้อง")

#         cleaned["user"] = user
#         return cleaned

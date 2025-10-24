from django import forms
import re
from django.contrib.auth.models import User
from room.models import Personnel
from django.contrib.auth import authenticate

class UserRegister(forms.Form):
    username = forms.CharField(label='Tên đăng nhập', max_length=20)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")
    
    def clean_confirm_password(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password == confirm_password and password:
                return password
        raise forms.ValidationError('Mật khẩu nhập lại không đúng')
    

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password'])

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Tên đăng nhập', max_length=20)
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())

    def display_errors(self):
        raise forms.ValidationError('Tên đăng nhập hoặc mật khẩu không đúng.')


class PersonnelRegister(forms.Form):
    username = forms.CharField(label='Tên đăng nhập', max_length=50)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^(NV)[0-9]+$', username):
            raise forms.ValidationError('Tài khoản nhân viên có dạng: NV1, NV2, NV42, ...')
        personnel = Personnel.objects.get(id_personnel=username)
        try:
            User.objects.get(username=personnel)
        except User.DoesNotExist:
            return username    
        raise forms.ValidationError('Tài khoản đã tồn tại')

    def clean_confirm_password(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password == confirm_password and password:
                return password
        raise forms.ValidationError('Mật khẩu nhập lại không đúng')
    
    def save(self):
        User.objects.create_user(username=self.clean_username(), email=self.cleaned_data['email'], password=self.clean_confirm_password())


class PersonnelLoginForm(forms.Form):
    username = forms.CharField(label='Tên đăng nhập', max_length=20)
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    
    
    
        
        
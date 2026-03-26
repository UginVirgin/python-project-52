# users/forms.py
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя (с паролем)"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'maxlength': '150'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия',
                'maxlength': '150'  # ← исправлено: maxlength, а не max_ength
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя',
                'maxlength': '150'
            }),
        }

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия', 
            'username': 'Имя пользователя'
        }

        error_messages = {
            'username': {
                'required': 'Имя пользователя обязательно',
                'unique': 'Пользователь с таким именем уже существует',
                'max_length': 'Имя не должно превышать 150 символов',
            },
        }
    
    def __init__(self, *args, **kwargs):
        """Добавляем виджеты для полей пароля"""
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля'
        })
        # Добавляем метки для полей пароля
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'


class CustomUserChangeForm(UserChangeForm):
    """Форма редактирования профиля пользователя (без пароля)"""
    
    password = None  # убираем поле пароля
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'maxlength': '150'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия',
                'maxlength': '150'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя',
                'maxlength': '150'
            }),
        }
        
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }
        
        error_messages = {
            'username': {
                'required': 'Имя пользователя обязательно',
                'unique': 'Пользователь с таким именем уже существует',
                'max_length': 'Имя не должно превышать 150 символов',
            },
        }
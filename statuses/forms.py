from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'maxlength': '100'
            })
        }
        
        labels = {
            'name': 'Имя'
        }
        
        error_messages = {
            'name': {
                'required': 'Пожалуйста, укажите имя статуса',
                'unique': 'Статус с таким именем уже существует', 
                'max_length': 'Имя не должно превышать 100 символов',
            }
        }
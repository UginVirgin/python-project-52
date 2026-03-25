from django import forms
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'max_lenght': '100'
            })
        }

        labels = {
            'name': 'Имя'
        }

        error_messages = {
            'name': {
            'required': 'Пожалуйста, укажите имя метки',
            'unique': 'Метка с таким именем уже существует', 
            'max_lenght': 'Имя не должно превышать 100 символов',
        }}
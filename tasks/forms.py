# tasks/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from statuses.models import Status
from labels.models import Label

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задачи'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Описание'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'executor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'labels': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
        }
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию'
        }),
        label='Имя'
    )
    
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Статус',
        empty_label='Все статусы'
    )
    
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Исполнитель',
        empty_label='Все исполнители'
    )
    
    labels = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Метка',
        empty_label='Все метки'
    )
    
    self_tasks = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Только мои задачи'
    )
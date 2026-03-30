# tasks/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from statuses.models import Status
from labels.models import Label

User = get_user_model()


class TaskForm(forms.ModelForm):
    # Явно определяем поле executor с кастомным отображением
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Исполнитель',
        required=False,
        empty_label="---------"
    )
    
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
            # Убираем executor из widgets, так как он определен выше
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Кастомное отображение опций: показываем full_name или username
        self.fields['executor'].label_from_instance = self.get_user_label
    
    def get_user_label(self, user):
        """Возвращает текст для отображения в выпадающем списке"""
        if user.get_full_name():
            return user.get_full_name()
        return user.username


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
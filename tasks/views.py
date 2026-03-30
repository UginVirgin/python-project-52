from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    DetailView
    )
from statuses.models import Status
from labels.models import Label
from tasks.models import Task
from .forms import TaskForm

User = get_user_model()


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        tasks = Task.objects.all()
        
        status_id = self.request.GET.get('status')
        executor_id = self.request.GET.get('executor')
        label_id = self.request.GET.get('label')
        self_tasks = self.request.GET.get('self_tasks')
        
        if status_id:
            tasks = tasks.filter(status_id=status_id)
        if executor_id:
            tasks = tasks.filter(executor_id=executor_id)
        if label_id:
            tasks = tasks.filter(labels__id=label_id)
        if self_tasks and self.request.user.is_authenticated:
            tasks = tasks.filter(creator=self.request.user)
        
        return tasks
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:tasks')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать задачу'
        context['button_text'] = 'Создать'
        return context
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно создана')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, '''
        Ошибка при создании задачи. Проверьте правильность заполнения полей.
        ''')
        return super().form_invalid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:tasks')
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить задачу'
        context['button_text'] = 'Изменить'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно изменена')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, '''
        Ошибка при изменении задачи. Проверьте правильность заполнения полей.
        ''')
        return super().form_invalid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks:tasks')
    pk_url_kwarg = 'id'
    
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.creator and not request.user.is_superuser:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks:tasks')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно удалена')
        return super().form_valid(form)
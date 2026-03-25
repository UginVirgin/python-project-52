from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Status
from .forms import StatusForm


class StatusListView(ListView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(CreateView):
    """Создание нового статуса"""
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:status_list')
    
    def form_valid(self, form):
        """При успешном создании статуса"""
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm 
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменен')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses:status_list')
    
    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(self.request, 'Невозможно удалить статус')
            return redirect('statuses:status_list')
        else:
            messages.success(self.request, 'Статус успешно удален')
            return super().form_valid(form)
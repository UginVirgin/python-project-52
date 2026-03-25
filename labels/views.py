from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from labels.models import Label
from .forms import LabelForm
from django.contrib import messages


class LabelListView(ListView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/labels.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно создана')
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm 
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешна изменена')
        return super().form_valid(form)


class DeleteLabelView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(self.request, 'Невозможно удалить метку')
            return redirect('labels:label_list')
        else:
            messages.success(self.request, 'Метка успешно удалена')
            return super().form_valid(form)
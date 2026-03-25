from django.shortcuts import render, redirect, get_object_or_404
from statuses.models import Status
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tasks.models import Task 
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Status
from .forms import StatusForm


def statuses(request):
    statuses = Status.objects.all()
    context = {'statuses': statuses}
    return render(request, 'statuses/statuses.html', context)


class StatusCreateView(CreateView):
    """Создание нового статуса"""
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:status_list')
    
    def form_valid(self, form):
        """При успешном создании статуса"""
        messages.success(self.request, f'Статус успешно создан!')
        return super().form_valid(form)



@login_required
def status_update(request, pk):
    status = get_object_or_404(Status, id=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            status.name = name
            status.save()
            messages.success(request, 'Статус успешно изменен')
            return redirect('statuses:status_list')
    
    return render(request, 'statuses/status_update.html', {
        'status': status
    })


@login_required
def status_delete(request, pk):
    status = get_object_or_404(Status, id=pk)
    
    if request.method == 'POST':
        if Task.objects.filter(status=status).exists():
            tasks_count = Task.objects.filter(status=status).count()
            messages.error(
                request, 
                f"""Невозможно удалить статус, потому что он 
                используется в {tasks_count} задаче(ах)"""
            )
            return redirect('statuses:status_list')
        
        status.delete()
        messages.success(request, 'Статус успешно удален')
        return redirect('statuses:status_list')
    
    return render(request, 'statuses/status_delete.html', {
        'status': status
    })
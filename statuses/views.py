from django.shortcuts import render, redirect, get_object_or_404
from statuses.models import Status
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tasks.models import Task 


def statuses(request):
    statuses = Status.objects.all()
    context = {'statuses': statuses}
    return render(request, 'statuses/statuses.html', context)


def status_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if Status.objects.filter(name=name).exists():
            context = {
                'error_name': 'Статус с таким именем уже существует',
                'form_data': {'name': name}
            }
            return render(request, 'statuses/status_create.html', context)
        
        try:
            Status.objects.create(name=name)
            messages.success(request, 'Статус успешно создан!')
            return redirect('statuses:status_list')
        except Exception as e:
            messages.error(request, f'Ошибка при создании статуса: {e}')
            context = {
                'error_name': str(e),
                'form_data': {'name': name}
            }
            return render(request, 'statuses/status_create.html', context)

    return render(request, 'statuses/status_create.html')


@login_required
def status_update(request, pk):
    status = get_object_or_404(Status, id=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            status.name = name
            status.save()
            messages.success(request, 'Статус успешно обновлен!')
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
                f'Невозможно удалить статус, потому что он используется в {tasks_count} задаче(ах)'
            )
            return redirect('statuses:status_list')
        
        status.delete()
        messages.success(request, 'Статус успешно удален!')
        return redirect('statuses:status_list')
    
    return render(request, 'statuses/status_delete.html', {
        'status': status
    })
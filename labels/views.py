from django.shortcuts import render, redirect, get_object_or_404
from labels.models import Label
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tasks.models import Task


def labels(request):
    labels = Label.objects.all()
    context = {'labels': labels}
    return render(request, 'labels/labels.html', context)


def label_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if Label.objects.filter(name=name).exists():
            context = {
                'error_name': 'Метка с таким именем уже существует',
                'form_data': {'name': name}
            }
            return render(request, 'labels/label_create.html', context)
        
        try:
            Label.objects.create(name=name)
            messages.success(request, 'Метка успешно создана!')
            return redirect('labels:label_list')
        except Exception as e:
            messages.error(request, f'Ошибка при создании метки: {e}')
            context = {
                'error_name': str(e),
                'form_data': {'name': name}
            }
            return render(request, 'labels/label_create.html', context)

    return render(request, 'labels/label_create.html')


@login_required
def label_update(request, pk):
    label = get_object_or_404(Label, id=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            label.name = name
            label.save()
            messages.success(request, 'Метка успешно обновлена!')
            return redirect('labels:label_list')
    
    return render(request, 'labels/label_update.html', {
        'label': label
    })



@login_required
def label_delete(request, pk):
    label = get_object_or_404(Label, id=pk)
    
    if request.method == 'POST':
        if Task.objects.filter(labels=label).exists():
            messages.error(
                request, 
                'Невозможно удалить метку, потому что она используется в задачах'
            )
            return redirect('labels:label_list')
        
        label.delete()
        messages.success(request, 'Метка успешно удалена!')
        return redirect('labels:label_list')
    
    return render(request, 'labels/label_delete.html', {
        'label': label
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from statuses.models import Status
from labels.models import Label
from tasks.models import Task
from users.models import AbstractUser


def tasks(request):
    tasks = Task.objects.all()
    
    status_id = request.GET.get('status')
    executor_id = request.GET.get('executor')
    label_id = request.GET.get('label')
    self_tasks = request.GET.get('self_tasks')
    
    if status_id:
        tasks = tasks.filter(status_id=status_id)
    if executor_id:
        tasks = tasks.filter(executor_id=executor_id)
    if label_id:
        tasks = tasks.filter(labels__id=label_id)
    if self_tasks and request.user.is_authenticated:
        tasks = tasks.filter(creator=request.user)
    
    context = {
        'tasks': tasks,
        'statuses': Status.objects.all(),
        'users': get_user_model().objects.all(),
        'labels': Label.objects.all(),
    }
    
    return render(request, 'tasks/tasks.html', context)


def create_task(request):
    if request.method == 'GET':
        statuses = Status.objects.all()
        User = get_user_model()
        executors = User.objects.all()
        labels = Label.objects.all()
        context = {
            'statuses': statuses,
            'executors': executors,
            "labels": labels
        }
        return render(request, "tasks/task_create.html", context)
    
    if request.method == 'POST':
        User = get_user_model()
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        status_id = request.POST.get('status')
        executor_id = request.POST.get('executor')
        labels_ids = request.POST.getlist('labels')
        
        errors = {}
        success = {}
        form_data = {
            'name': name,
            'description': description,
            'status': status_id,
            'executor': executor_id,
            'labels': labels_ids
        }
        
        # Валидация имени
        if not name or not name.strip():
            errors['name'] = 'Имя задачи не может быть пустым'
        elif Task.objects.filter(name=name).exists():
            errors['name'] = 'Задача с таким именем уже существует'
        else:
            success['name'] = '✓ Имя введено корректно'
        
        # Валидация описания (опционально)
        if description and len(description) < 3:
            errors['description'] = 'Описание должно содержать минимум 3 символа'
        elif description:
            success['description'] = '✓ Описание заполнено'
        else:
            success['description'] = '✓ Описание не заполнено'
        
        # Валидация статуса
        if not status_id:
            errors['status'] = 'Необходимо выбрать статус'
        else:
            try:
                status = Status.objects.get(id=status_id)
                success['status'] = '✓ Статус выбран'
            except Status.DoesNotExist:
                errors['status'] = 'Выбранный статус не существует'
        
        # Валидация исполнителя
        if executor_id:
            try:
                executor = User.objects.get(id=executor_id)
                success['executor'] = f'✓ Исполнитель: {executor.get_full_name() or executor.username}'
            except User.DoesNotExist:
                errors['executor'] = 'Выбранный исполнитель не существует'
        else:
            executor = None
            success['executor'] = '✓ Исполнитель не назначен'
        
        # Валидация меток
        if labels_ids:
            valid_labels = Label.objects.filter(id__in=labels_ids)
            if len(valid_labels) != len(labels_ids):
                errors['labels'] = 'Некоторые выбранные метки не существуют'
            else:
                success['labels'] = f'✓ Выбрано меток: {len(labels_ids)}'
        else:
            success['labels'] = '✓ Метки не выбраны'
        
        if errors:
            statuses = Status.objects.all()
            executors = User.objects.all()
            labels = Label.objects.all()
            
            context = {
                'errors': errors,
                'success': success,
                'form_data': form_data,
                'statuses': statuses,
                'executors': executors,
                'labels': labels
            }
            return render(request, "tasks/task_create.html", context)
        
        try:
            status = Status.objects.get(id=status_id)
            executor = User.objects.get(id=executor_id) if executor_id else None
            
            task = Task.objects.create(
                name=name, 
                description=description,
                status=status,
                executor=executor,
                creator=request.user
            )
            
            if labels_ids:
                task.labels.set(labels_ids)
            
            messages.success(request, 'Задача успешно создана!')
            return redirect('tasks:tasks')
            
        except Exception as e:
            messages.error(request, f'Ошибка при создании задачи: {e}')
            
            statuses = Status.objects.all()
            executors = User.objects.all()
            labels = Label.objects.all()
            
            context = {
                'errors': {'general': str(e)},
                'success': success,
                'form_data': form_data,
                'statuses': statuses,
                'executors': executors,
                'labels': labels
            }
            return render(request, "tasks/task_create.html", context)
            
            
def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    context = {
        'task': task
    }
    return render(request, "tasks/task_detail.html", context)


def task_update(request, id):
    task = get_object_or_404(Task, id=id)
    
    if request.method == 'GET':
        statuses = Status.objects.all()
        User = get_user_model()
        executors = User.objects.all()
        labels = Label.objects.all()
        context = {
            'task': task,
            'statuses': statuses,
            'executors': executors,
            'labels': labels
        }
        return render(request, "tasks/task_update.html", context)
    
    if request.method == 'POST':
        User = get_user_model()
        
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            status_id = request.POST.get('status')
            executor_id = request.POST.get('executor')
            labels_ids = request.POST.getlist('labels')
            
            if Task.objects.filter(name=name).exclude(id=task.id).exists():
                messages.error(request, 'Задача с таким именем уже существует')
                
                statuses = Status.objects.all()
                executors = User.objects.all()
                labels = Label.objects.all()
                context = {
                    'task': task,
                    'statuses': statuses,
                    'executors': executors,
                    'labels': labels,
                    'form_data': request.POST
                }
                return render(request, "tasks/task_update.html", context)
            
            task.name = name
            task.description = description
            task.status = Status.objects.get(id=status_id) if status_id else None
            task.executor = User.objects.get(id=executor_id) if executor_id else None
            
            task.save()
            
            if labels_ids:
                task.labels.set(labels_ids)
            else:
                task.labels.clear()
            
            messages.success(request, 'Задача успешно изменена!')
            return redirect('tasks:tasks')
            
        except Exception as e:
            messages.error(request, f'Ошибка при изменении задачи: {e}')
            
            statuses = Status.objects.all()
            executors = User.objects.all()
            labels = Label.objects.all()
            context = {
                'task': task,
                'statuses': statuses,
                'executors': executors,
                'labels': labels,
                'form_data': request.POST
            }
            return render(request, "tasks/task_update.html", context)


def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    
    if request.method == 'POST':
        if request.user == task.creator or request.user.is_superuser:
            task.delete()
            messages.success(request, 'Задача успешно удалена!')
        else:
            messages.error(request, 'У вас нет прав для удаления этой задачи')
        
        return redirect('tasks:tasks')
    
    return render(request, 'tasks/task_delete.html', {'task': task})

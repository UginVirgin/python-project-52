from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from statuses.models import Status
from labels.models import Label
from tasks.models import Task
from users.models import AbstractUser # noqa: F401


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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from statuses.models import Status
from labels.models import Label
from tasks.models import Task


def create_task(request):
    if request.method == 'GET':
        return handle_get_create_task(request)
    elif request.method == 'POST':
        return handle_post_create_task(request)


def handle_get_create_task(request):
    User = get_user_model()
    context = {
        'statuses': Status.objects.all(),
        'executors': User.objects.all(),
        'labels': Label.objects.all()
    }
    return render(request, "tasks/task_create.html", context)


def handle_post_create_task(request):
    User = get_user_model()
    form_data = extract_form_data(request)
    validation_result = validate_task_data(request, form_data, User)
    
    if validation_result['errors']:
        return render_with_errors(request, form_data, validation_result)
    
    return create_new_task(request, form_data, validation_result, User)


def extract_form_data(request):
    return {
        'name': request.POST.get('name'),
        'description': request.POST.get('description'),
        'status_id': request.POST.get('status'),
        'executor_id': request.POST.get('executor'),
        'labels_ids': request.POST.getlist('labels')
    }


def validate_task_data(request, form_data, User):
    errors = {}
    success = {}
    
    validate_name(form_data['name'], errors, success)
    validate_description(form_data['description'], errors, success)
    status = validate_status(form_data['status_id'], errors, success)
    executor = validate_executor(form_data['executor_id'], errors, success, User)
    validate_labels(form_data['labels_ids'], errors, success)
    
    return {
        'errors': errors,
        'success': success,
        'status': status,
        'executor': executor
    }


def validate_name(name, errors, success):
    if not name or not name.strip():
        errors['name'] = 'Имя задачи не может быть пустым'
    elif Task.objects.filter(name=name).exists():
        errors['name'] = 'Задача с таким именем уже существует'
    else:
        success['name'] = '✓ Имя введено корректно'


def validate_description(description, errors, success):
    if description and len(description) < 3:
        errors['description'] = 'Описание должно содержать минимум 3 символа'
    elif description:
        success['description'] = '✓ Описание заполнено'
    else:
        success['description'] = '✓ Описание не заполнено'


def validate_status(status_id, errors, success):
    if not status_id:
        errors['status'] = 'Необходимо выбрать статус'
        return None
    
    try:
        status = Status.objects.get(id=status_id)
        success['status'] = '✓ Статус выбран'
        return status
    except Status.DoesNotExist:
        errors['status'] = 'Выбранный статус не существует'
        return None


def validate_executor(executor_id, errors, success, User):
    if not executor_id:
        success['executor'] = '✓ Исполнитель не назначен'
        return None
    
    try:
        executor = User.objects.get(id=executor_id)
        success['executor'] = f'✓ Исполнитель: {executor.get_full_name() or executor.username}'
        return executor
    except User.DoesNotExist:
        errors['executor'] = 'Выбранный исполнитель не существует'
        return None


def validate_labels(labels_ids, errors, success):
    if labels_ids:
        valid_labels = Label.objects.filter(id__in=labels_ids)
        if len(valid_labels) != len(labels_ids):
            errors['labels'] = 'Некоторые выбранные метки не существуют'
        else:
            success['labels'] = f'✓ Выбрано меток: {len(labels_ids)}'
    else:
        success['labels'] = '✓ Метки не выбраны'


def render_with_errors(request, form_data, validation_result):
    User = get_user_model()
    context = {
        'errors': validation_result['errors'],
        'success': validation_result['success'],
        'form_data': form_data,
        'statuses': Status.objects.all(),
        'executors': User.objects.all(),
        'labels': Label.objects.all()
    }
    return render(request, "tasks/task_create.html", context)


def create_new_task(request, form_data, validation_result, User):
    try:
        task = Task.objects.create(
            name=form_data['name'],
            description=form_data['description'],
            status=validation_result['status'],
            executor=validation_result['executor'],
            creator=request.user
        )
        
        if form_data['labels_ids']:
            task.labels.set(form_data['labels_ids'])
        
        messages.success(request, 'Задача успешно создана!')
        return redirect('tasks:tasks')
        
    except Exception as e:
        messages.error(request, f'Ошибка при создании задачи: {e}')
        
        context = {
            'errors': {'general': str(e)},
            'success': validation_result['success'],
            'form_data': form_data,
            'statuses': Status.objects.all(),
            'executors': User.objects.all(),
            'labels': Label.objects.all()
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

            if status_id:
                task.status = Status.objects.get(id=status_id)
            else:
                task.status = None

            if executor_id:
                task.executor = User.objects.get(id=executor_id)
            else:
                task.executor = None
            
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
    
    if request.user != task.creator and not request.user.is_superuser:
        messages.error(request, 'Задачу может удалить только ее автор')
        return redirect('tasks:tasks')
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect('tasks:tasks')
    
    return render(request, 'tasks/task_delete.html', {'task': task})

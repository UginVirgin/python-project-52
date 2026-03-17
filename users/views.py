from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def users(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'users/users.html', context={'users': users})


def users_create(request):
    form_data = request.POST if request.method == 'POST' else None
    errors = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        if password1 != password2:
            errors['password2'] = 'Пароли не совпадают'
        
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Пользователь с таким именем уже существует'
        
        if not username:
            errors['username'] = 'Имя пользователя обязательно'
        
        if not errors:
            try:
                User.objects.create_user(
                    username=username,
                    password=password1,
                    first_name=request.POST.get('first_name', ''),
                    last_name=request.POST.get('last_name', ''),
                    email=email
                )
                messages.success(request, 'Пользователь успешно зарегистрирован')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Ошибка: {e}')
        
        form_data = request.POST
    
    return render(request, 'users/create_user.html', {
        'form_data': form_data,
        'errors': errors
    })


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        if not username:
            messages.error(request, 'Имя пользователя обязательно')
            return render(request, 'users/user_update.html', {'user': user})
        
        if User.objects.filter(username=username).exclude(pk=pk).exists():
            messages.error(request, 'Имя пользователя уже занято')
            return render(request, 'users/user_update.html', {'user': user})
        
        user.username = username
        user.email = email
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        
        messages.success(request, 'Пользователь обновлен')
        return redirect('users:users')
    
    return render(request, 'users/user_update.html', {'user': user})


@login_required
def user_profile(request):
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    """LoginView с флеш-сообщением"""
    
    def form_valid(self, form):
        """При успешном входе"""
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)
    

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Проверка прав - пользователь может удалить только себя
    if request.user.id != user.id:
        messages.error(request, 'У вас нет прав для удаления этого пользователя')
        return redirect('users:users')
    
    if request.method == 'POST':
        # Дополнительная проверка: нельзя удалить последнего админа
        if user.is_superuser and User.objects.filter(is_superuser=True).count() == 1:
            messages.error(request, 'Нельзя удалить последнего администратора')
            return redirect('users:users')
        
        username = user.username
        user.delete()
        messages.success(request, f'Пользователь {username} успешно удален')
        return redirect('users:users')
    
    return render(request, 'users/user_delete.html', {'user': user})


class CustomLogoutView(LogoutView):
    """LogoutView с флеш-сообщением"""
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
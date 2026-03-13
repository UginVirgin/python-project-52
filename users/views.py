from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def users(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'users/users.html', context={'users': users})


def users_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'users/create_user.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'users/create_user.html')
        
        try:
            User.objects.create_user(
                username=username,
                password=password1,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                email=email
            )
            messages.success(request, 'Пользователь успешно создан!')
            return redirect('users')
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')
    
    return render(request, 'users/create_user.html')


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
        return redirect('users')
    
    return render(request, 'users/user_update.html', {'user': user})


@login_required
def user_profile(request):
    return render(request, 'auth_base.html')

class CustomLogoutView(LogoutView):
    """LogoutView с флеш-сообщением"""
    
    def dispatch(self, request, *args, **kwargs):
        # Добавляем сообщение перед выходом
        messages.success(request, 'Вы успешно вышли из системы!')
        return super().dispatch(request, *args, **kwargs)
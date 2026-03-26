from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy


def index(request):
    return render(request, 'index.html')


class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'
    ordering = ['username']


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при регистрации. Проверьте правильность заполнения.')
        return super().form_invalid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:users')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно обновлен')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при обновлении. Проверьте правильность заполнения.')
        return super().form_invalid(form)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('users:profile') 
    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:users')
    context_object_name = 'user'
    
    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if request.user.id != self.object.id:
            messages.error(request, 'У вас нет прав для удаления этого пользователя')
            return redirect('users:users')
        
        if self.object.is_superuser:
            admin_count = User.objects.filter(is_superuser=True).count()
            if admin_count == 1:
                messages.error(request, 'Нельзя удалить последнего администратора')
                return redirect('users:users')
        
        username = self.object.username
        messages.success(request, f'Пользователь "{username}" успешно удален')
        return super().delete(request, *args, **kwargs)


class CustomLogoutView(LogoutView):    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
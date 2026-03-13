from django.db import models
from django.contrib.auth import get_user_model
from statuses.models import Status
from labels.models import Label

User = get_user_model()

class Task(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя задачи'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Подробное описание задачи'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Дата обновления'
    )
    
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус',
        related_name='tasks'
    )
    
    # Связь с метками (МНОГИЕ ко МНОГИМ, а не ForeignKey)
    labels = models.ManyToManyField(  # Измените на ManyToManyField
        Label,
        blank=True,  # Может быть без меток
        verbose_name='Метки',
        related_name='tasks'  # label.tasks.all()
    )
    
    # Связь с создателем
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='created_tasks'  # user.created_tasks.all()
    )
    
    # Добавьте исполнителя (опционально)
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # При удалении пользователя - сделать NULL
        null=True,
        blank=True,
        verbose_name='Исполнитель',
        related_name='assigned_tasks'  # user.assigned_tasks.all()
    )
    
    def __str__(self):
        return f'{self.name} ({self.status.name if self.status else "без статуса"})'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
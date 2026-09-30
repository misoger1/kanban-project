from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название доски")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    title = models.CharField(max_length=50, verbose_name="Название колонки")
    slug = models.CharField(max_length=20) # 'todo', 'in_progress', 'done'
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.board.title})"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium', verbose_name="Приоритет")
    deadline = models.DateField(blank=True, null=True, verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
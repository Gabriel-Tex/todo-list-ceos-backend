from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ('low','BAIXA'),
    ('medium', 'MEDIA'),
    ('high', 'ALTA'),
]

STATUS_CHOICES = [
    ('pending',   'PENDENTE'),
    ('completed', 'CONCLUÍDA'),
]

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='tasks')
    final_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} [{self.get_status_display()}]'
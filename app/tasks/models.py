from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ('low','BAIXA'),
    ('medium', 'MEDIA'),
    ('high', 'ALTA'),
]

class Tasks(models.Model):
    tittle = models.CharField(max_length=50)
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    final_date = models.DateField(blank=True,null=True)


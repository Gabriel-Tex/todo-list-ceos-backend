from rest_framework import serializers
from .models import Task, PRIORITY_CHOICES, STATUS_CHOICES


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True) 
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 'owner', 'final_date', 'created_at',]

from rest_framework import serializers
from .models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'priority', 'owner', 'final_date']

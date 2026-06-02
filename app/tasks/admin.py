from django.contrib import admin
from tasks.models import Tasks

@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('tittle','priority','owner','final_date')
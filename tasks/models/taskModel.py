from django.db import models
from tasks.models.taskListModel import TaskList
class Task(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated ID
    title = models.CharField(max_length=255)  # Task title
    description = models.TextField(blank=True, null=True)  # Optional description
    is_completed = models.BooleanField(default=False)  # Completion status
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks")  

    def __str__(self):
        return self.title

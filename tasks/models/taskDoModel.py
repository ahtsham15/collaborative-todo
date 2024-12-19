from django.db import models
from tasks.models.taskListModel import TaskList

class TaskDo(models.Model):
    id = models.AutoField(primary_key=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
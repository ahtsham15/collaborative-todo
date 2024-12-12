from django.db import models
from tasks.models.userModel import User

class TaskList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_task_lists")
    shared_with = models.ManyToManyField(User, related_name="shared_task_lists", blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name
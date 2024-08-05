from django.contrib.auth.models import User
from django.db import models

from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               null=False, blank=False,
                               related_name='status_tasks')
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='author_tasks')
    executor = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='executor_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

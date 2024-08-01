from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

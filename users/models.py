from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username
# Create your models here.

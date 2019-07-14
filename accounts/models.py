from django.db import models


class User(models.Model):
    message = models.CharField(max_length=200)

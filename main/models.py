from django.db import models

class Task(model.Model):
    question = models.CharField(max_length=200)
    date = models.DateTimeField('date')
    answer = models.CharField(max_length=100)

class User(model.Model):
    access = models.IntegerField()
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=32) # MD5 hash


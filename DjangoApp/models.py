from django.db import models


# Create your models here.

# class TodoItem(models.Model):
#     title = models.CharField(max_length=200)
#     completed = models.BooleanField(default=False)


class Skill(models.Model):
    image = models.ImageField(upload_to='skills/')


class Demand(models.Model):
    image = models.ImageField(upload_to='demand/')


class Geography(models.Model):
    image = models.ImageField(upload_to='geography/')

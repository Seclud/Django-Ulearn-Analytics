from django.db import models


# Create your models here.

# class TodoItem(models.Model):
#     title = models.CharField(max_length=200)
#     completed = models.BooleanField(default=False)


# class Skill(models.Model):
#     image = models.ImageField(upload_to='skills/')
#
#
# class Demand(models.Model):
#     image = models.ImageField(upload_to='demand/')
#
#
# class Geography(models.Model):
#     image = models.ImageField(upload_to='geography/')

class Image(models.Model):
    class Category(models.TextChoices):
        SKILL = 'SK', 'Skills'
        DEMAND = 'DM', 'Demand'
        GEOGRAPHY = 'GR', 'Geography'

    category = models.CharField(max_length=2, choices=Category.choices)
    image = models.ImageField(upload_to='images/')

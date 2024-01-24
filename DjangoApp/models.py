from django.db import models


# Create your models here.

class Image(models.Model):
    class Category(models.TextChoices):
        SKILL = 'SK', 'Skills'
        DEMAND = 'DM', 'Demand'
        GEOGRAPHY = 'GR', 'Geography'

    category = models.CharField(max_length=2, choices=Category.choices)
    image = models.ImageField(upload_to='images/')


class DataTable(models.Model):
    class Category(models.TextChoices):
        SKILL = 'SK', 'Skills'
        DEMAND = 'DM', 'Demand'
        GEOGRAPHY = 'GR', 'Geography'

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=Category.choices)
    csv_file = models.FileField(upload_to='csvs/')

from django.db import models

# Create your models here.

class User(models.Model):
    restaurant_name = models.CharField(max_length=100)
    restaurant_link = models.CharField(max_length=500)
    restaurant_content = models.TextField()
    restaurant_keyword = models.CharField(max_length=50)
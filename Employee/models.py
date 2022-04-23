from django.db import models

# Create your models here.
class EmpLogin(models.Model):
    user_id = models.CharField(max_length=70)
    password = models.CharField(max_length=50)

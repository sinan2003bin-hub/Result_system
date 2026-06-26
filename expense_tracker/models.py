from django.db import models
from django.utils import timezone   
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.name
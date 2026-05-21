# pyright: reportMissingModuleSource=false
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(null=True, blank=True)
    subject = models.CharField(max_length=100,null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
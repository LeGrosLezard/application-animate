"""This is model from accounts app"""

from django.db import models

class Accounts(models.Model):
    """foodAccount model"""
    
    name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)



    

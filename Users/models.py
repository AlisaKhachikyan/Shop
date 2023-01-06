from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()
    date_of_birth=models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email

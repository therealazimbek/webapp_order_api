from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    fullname = models.CharField(max_length=200)
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def calculate_age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))


STATUS_CHOICES = (
    ("1", "Sent"),
    ("2", "Rejected"),
    ("3", "Contact you soon"),
    ("4", "Being developed")
)


class Order(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return str(self.title)

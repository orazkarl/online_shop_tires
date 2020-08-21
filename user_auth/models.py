from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

# Create your models here.
class User(AbstractUser):
    email = models.EmailField('E-mail', max_length=100, unique=True)
    phone_number = models.CharField('Телефон', max_length=250)
    city = models.CharField('Город', max_length=100, null=True)
    address = models.CharField('Адрес', max_length=100, null=True)
    wishlist_counter = models.PositiveIntegerField(default=0)
    cart_counter = models.PositiveIntegerField(default=0)


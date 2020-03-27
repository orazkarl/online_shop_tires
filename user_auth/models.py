from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

# Create your models here.
class User(AbstractUser):
    email = models.EmailField('E-mail', max_length=100, unique=True)
    phone_number = models.PositiveIntegerField('Телефон', validators=[MaxValueValidator(99999999999)], null=True)
    city = models.CharField('Город', max_length=100, null=True)
    address = models.CharField('Адрес', max_length=100, null=True)


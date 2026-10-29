from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    # Campo extra de la practica: telefono de contacto del cliente
    telefono = models.CharField(
        max_length=10,
        blank=True,
        validators=[RegexValidator(r'^\d{10}$', 'El telefono debe tener 10 digitos.')],
        verbose_name='Telefono',
        help_text='10 digitos, sin espacios ni guiones.',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

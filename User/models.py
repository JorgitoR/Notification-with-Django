from django.contrib.auth.models import AbstractUser

# Django
from django.db import models

class Usuario(AbstractUser):
	lector =  models.BooleanField(default=True)




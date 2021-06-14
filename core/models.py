from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=55)
    email = models.EmailField(max_length=55)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class Joueurs(models.Model):
    nom = models.CharField(max_length=255)
    age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'joueurs'
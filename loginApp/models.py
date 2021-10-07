from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings

# Create your models here.


class Storage(models.Model):
    def __str__(self):
        return f"{self.pk}"


class APIModel(models.Model):
    id = models.AutoField(unique=True, blank=False, primary_key=True, auto_created=True)
    username = models.CharField(max_length=200, unique=True, blank=False)
    rfid_id = models.CharField(max_length=200, unique=True, blank=False)
    crd = models.DateTimeField(blank=False, auto_now_add=True)
    valid_to = models.DateTimeField(blank=False, default=timezone.now() + timezone.timedelta(minutes=5))


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    is_moderator = models.BooleanField(default=False)
    storage = models.OneToOneField(Storage, null=True, on_delete=models.SET_NULL)
    rfid_id = models.CharField(max_length=20, blank=True, default=None, null=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']


class Allergies(models.Model):
    name = models.CharField(max_length=200, unique=True)
    tej = models.BooleanField()
    gluten = models.BooleanField()
    hus = models.BooleanField()
    tojas = models.BooleanField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty = models.IntegerField()
    description = models.TextField()
    allergies = models.ForeignKey(Allergies, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(blank=True, null=True, default=None, upload_to="recipes")

    def mask_pk(self):
        return settings.FERNET.encrypt(str(self.pk).encode()).decode()

    def __str__(self):
        return f"{self.name} ({self.allergies})"


class PreIngredients(models.Model):
    group = models.IntegerField()
    measure = models.CharField(max_length=200)
    multiply = models.IntegerField()

    def __str__(self):
        return self.measure


class AllIngredients(models.Model):
    name = models.CharField(max_length=200)
    group = models.IntegerField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    measure = models.DecimalField(max_digits=10, decimal_places=2)
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING, blank=True, null=True)
    storage = models.ForeignKey(Storage, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"{self.name}: \t{self.measure} {self.unit}"

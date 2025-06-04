from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone

class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=40, verbose_name='Enter your manufacturer\'s name')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='manufacturers')

    def __str__(self):
        return f"{self.name}"


class CarEngine(models.Model):
    name = models.CharField(max_length=30)
    horse_power = models.IntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='engines')
    release_date = models.DateField()

    def __str__(self):
        return self.name


class Car(models.Model):
    car_model = models.CharField(max_length=30)
    engine_model = models.ForeignKey(CarEngine, on_delete=models.CASCADE, related_name='cars')
    serial_number = models.CharField(max_length=70, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='cars')
    release_date = models.DateField()
    car_image = models.ImageField(upload_to='car_images/', null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.manufacturer} {self.car_model} ({self.engine_model})"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        ordering = ('-manufacturer', )



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Incorrect email in models")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    register_date = models.DateField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class MobileNumberField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        value_str = str(value)
        if not value_str.isdigit():
            raise ValidationError('Mobile number must contain only digits.')
        if len(value_str) != 10:
            raise ValidationError('Mobile number must be 10 digits long.')
        return value


class PinCodeField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        value_str = str(value)
        if not value_str.isdigit():
            raise ValidationError('Mobile number must contain only digits.')
        if len(value_str) != 6:
            raise ValidationError('Mobile number must be 6 digits long.')
        return value
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('author', 'Author'),
    ]
    first_name = models.CharField(max_length=30, help_text='Required. Enter your first name.')
    last_name = models.CharField(max_length=30, help_text='Required. Enter your last name.')
    mobile_number = MobileNumberField(help_text='Required. Enter your mobile number.')
    email = models.EmailField(unique=True, max_length=254, help_text='Required. Enter a valid email address.')
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, help_text='are you a admin or author')
    pincode = PinCodeField(help_text='Enter your Pin Code')
    username = models.CharField(unique=True, default='default_username', max_length=30, help_text='Required. Enter your username.')
    passkey = models.CharField(max_length=100, help_text='Required. Enter your password.')

    class Meta:
        app_label = 'content'

    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    
    def __str__(self):
        return self.username

class Blog(models.Model):
    title = models.CharField(unique=True, max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=60)
    category = models.CharField(max_length=100)
    createdBy = models.CharField(max_length=60)

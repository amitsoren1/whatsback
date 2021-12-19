from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.utils import timezone

from .managers import CustomUserManager

def validate_phone(value):
    value = str(value)
    if not value.isnumeric:
        raise ValidationError(
            _('%(value)s is not a number'),
            params={'value': value},
        )
    if len(value)!=10 or value[0]==0:
        raise ValidationError(
            _('%(value)s is not a valid phone number'),
            params={'value': value},
        )


class User(AbstractUser):
    phone = models.IntegerField(_("phone number"), unique=True, validators=[validate_phone])
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    username = None
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.phone}"

def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"profile_pictures/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(_("Avatar"), upload_to=upload_to, blank=True)
    whatsapp_name = models.CharField(max_length=20, blank=True, default="phone")
    whatsapp_status = models.CharField(max_length=100, blank=True, default="Hi there! I am using whatsapp")
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.phone}"


class Contact(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contacts", unique=False)
    name = models.CharField(max_length=255)
    phone = models.IntegerField(_("phone number"), unique=True, validators=[validate_phone])
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"

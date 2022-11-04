from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.utils.translation import gettext_lazy as _
GENDER_TYPES = (
    ("male", "male"),
    ("female", "female"),
    ("x", "not known"),
)


# Create your models here.

class User(AbstractUser):
    middle_name = models.CharField("middle_name", max_length=256, blank=True)

    gender = models.CharField(max_length=15, choices=GENDER_TYPES, default=GENDER_TYPES[2][0])
    birth_date = models.DateField(null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=32, blank=True)
    image = models.ImageField(upload_to='user', null=True)

    created_at = models.DateTimeField("date created", auto_now_add=True, null=True)
    updated_at = models.DateTimeField("date updated", auto_now=True)

    is_agree = models.BooleanField(default=False)

    class Meta:
        db_table = "user"
        swappable = "AUTH_USER_MODEL"
        verbose_name = "user"
        verbose_name_plural = "users"

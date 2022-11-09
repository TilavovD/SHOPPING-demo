from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from django.apps import apps
from django.utils.translation import gettext_lazy as _

GENDER_TYPES = (
    ("male", "male"),
    ("female", "female"),
    ("x", "not known"),
)


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone number must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    middle_name = models.CharField(_("middle_name"), max_length=256, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_TYPES, default=GENDER_TYPES[2][0])
    birth_date = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(_("phone number"),
                                    max_length=20,
                                    unique=True,
                                    error_messages={
                                        "unique": _("A user with that phone number already exists."),
                                    },
                                    )
    city = models.CharField(max_length=32, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)
    objects = CustomUserManager()
    created_at = models.DateTimeField("date created", auto_now_add=True, null=True)
    updated_at = models.DateTimeField("date updated", auto_now=True)

    is_agree = models.BooleanField(default=False)

    username = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)




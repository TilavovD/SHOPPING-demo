from django.contrib import admin
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'phone_number':
            kwargs['widget'] = PhoneNumberPrefixWidget
        return super(UserAdmin, self).formfield_for_dbfield(db_field, **kwargs)

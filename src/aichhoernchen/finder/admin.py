# Register your models here.
from django.contrib import admin

from .models import FoundObject, LostPropertyOffice

admin.site.register(FoundObject)
admin.site.register(LostPropertyOffice)

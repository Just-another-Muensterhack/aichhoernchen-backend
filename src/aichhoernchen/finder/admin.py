# Register your models here.
from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import Finder, FoundObject, LostPropertyOffice


class FoundObjectInline(StackedInline):
    model = FoundObject


@admin.register(Finder)
class FinderAdmin(ModelAdmin):
    inlines = [FoundObjectInline]


admin.site.register(LostPropertyOffice)

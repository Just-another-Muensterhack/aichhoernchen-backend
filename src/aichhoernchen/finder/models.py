from django.db import models


class FoundObject(models.Model):
    short_title = models.TextField()
    long_title = models.TextField()
    description = models.TextField()
    lat = models.FloatField()
    long = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    finder_name = models.TextField()
    finder_email = models.EmailField()
    finder_phone = models.TextField()
    deposit = models.ForeignKey("LostPropertyOffice", related_name="objects", on_delete=models.SET_NULL, null=True, blank=True)


class LostPropertyOffice(models.Model):
    name = models.TextField()
    email = models.EmailField()
    phone = models.TextField()
    address = models.TextField()
    link = models.TextField(null=True, blank=True)
    lat = models.FloatField()
    long = models.FloatField()

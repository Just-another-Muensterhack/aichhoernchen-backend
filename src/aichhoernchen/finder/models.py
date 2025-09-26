from django.db import models


class FoundObject(models.Model):
    short_title = models.TextField()
    long_title = models.TextField()
    description = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    finder = models.OneToOneField("Finder", on_delete=models.CASCADE)
    deposit = models.ForeignKey("LostPropertyOffice", on_delete=models.SET_NULL, null=True, blank=True)


class Finder(models.Model):
    name = models.TextField()
    email = models.EmailField()
    phone = models.TextField()


class LostPropertyOffice(models.Model):
    name = models.TextField()
    email = models.EmailField()
    phone = models.TextField()
    address = models.TextField()
    link = models.TextField(null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)

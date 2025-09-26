from django.db import models


class FoundObject(models.Model):
    short_title = models.TextField()
    long_title = models.TextField()
    description = models.TextField()
    lat = models.DecimalField()
    long = models.DecimalField()
    timestampt = models.DateTimeField(auto_now_add=True)
    finder = models.ForeignKey("Finder", on_delete=models.CASCADE)


class Finder(models.Model):
    name = models.TextField()

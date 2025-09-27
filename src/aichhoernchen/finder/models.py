from hashlib import sha1

from django.db import models


class LostPropertyOffice(models.Model):
    name = models.TextField()
    email = models.EmailField()
    phone = models.TextField()
    address = models.TextField()
    link = models.TextField(null=True, blank=True)
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self) -> str:
        return f"{self.name} ({self.address})"


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
    verified = models.BooleanField(default=False)
    deposit = models.ForeignKey(LostPropertyOffice, related_name="found_objects", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.finder_name} found {self.short_title} at {self.timestamp}"


    @property
    def anonymized_name(self) -> str:
        return f"{self.finder_name[0]}{"*" * 9}"

    @property
    def anonymized_email(self) -> str:
        domain = "aichhoernchen.de"

        sha1_hash = sha1(self.finder_email.encode('utf-8')).hexdigest()
        return f"{sha1_hash[:10]}@{domain}"

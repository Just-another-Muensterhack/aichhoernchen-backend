import json
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import FoundObject, LostPropertyOffice


class Command(BaseCommand):
    help = "Imports default data for lost property offices."


    def handle(self, *args: Any, **options: Any) -> None:
        objects = set(FoundObject.objects.all().values_list("description", flat=True))
        muenster_office = LostPropertyOffice.objects.get(name="Stadt Münster")

        with open(settings.BASE_DIR / "finder" / "static" / "objects.json", "r") as json_file:
            data = json.load(json_file)
            FoundObject.objects.filter(description__in=objects).delete()

            for object in data:
                FoundObject.objects.update_or_create(
                    short_title=object.get("short_title", ""),
                    long_title=object.get("long_title", ""),
                    description=object.get("description", ""),
                    lat=object.get("lat", 0.0),
                    long=object.get("lng", 0.0),
                    timestamp=f"{object.get("timestamp", "2023-01-01T00:00:00")}+00:00",
                    finder_name=object.get("finder_name", ""),
                    finder_email=object.get("finder_email", ""),
                    finder_phone=object.get("finder_phone", ""),
                    verified=True,
                    deposit=muenster_office,
                )

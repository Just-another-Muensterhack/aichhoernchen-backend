import json
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import LostPropertyOffice


class Command(BaseCommand):
    help = "Imports default data for lost property offices."


    def handle(self, *args: Any, **options: Any) -> None:
        deposits = set(LostPropertyOffice.objects.all().values_list("name", flat=True))
        with open(settings.BASE_DIR / "finder" / "static" / "offices.json", "r") as json_file:
            data = json.load(json_file)
            LostPropertyOffice.objects.filter(name__in=deposits).delete()

            for office in data:
                LostPropertyOffice.objects.update_or_create(
                    name=office.get("name", ""),
                    email=office.get("email", ""),
                    phone=office.get("phone", ""),
                    address=f"{office.get("street", "")}, {office.get('zip_city', '')}",
                    link=office.get("webseite", ""),
                    lat=office.get("lat", 0.0),
                    long=office.get("lng", 0.0),
                )

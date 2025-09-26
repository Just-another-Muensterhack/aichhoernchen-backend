from __future__ import annotations

import strawberry
import strawberry_django

from ..types import FoundObjectType, LostPropertyOfficeType


@strawberry.type
class Query:
    found_object: FoundObjectType = strawberry.field()
    found_objects: list[FoundObjectType] = strawberry_django.field()

    lost_property_office: LostPropertyOfficeType = strawberry.field()
    lost_property_offices: list[LostPropertyOfficeType] = strawberry_django.field()

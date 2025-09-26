from __future__ import annotations

from typing import Optional

from django.db.models import QuerySet
from geopy.distance import distance
from strawberry import auto
from strawberry_django import filter_type, order_type
from strawberry_django import input as graphql_input
from strawberry_django import type as graphql_type
from strawberry_django.filters import filter as graphql_filter

from .models import FoundObject, LostPropertyOffice


# filters
@graphql_input
class LocationInput:
    lat: float
    long: float
    distance: float

@graphql_filter
class LocationFilter:
    location: LocationInput

    def filter_location(
        self,
        queryset: QuerySet,
    ) -> QuerySet:
        filtered_obj = []
        for obj in queryset:
            obj_distance = distance((self.location.lat, self.location.long), (obj.lat, obj.long)).km
            if obj_distance <= self.location.distance:
                filtered_obj.append(obj.pk)
        return queryset.filter(pk__in=filtered_obj)


@filter_type(FoundObject, lookups=True)
class FoundObjectFilter:
    short_title: auto
    long_title: auto
    description: auto
    lat: auto
    long: auto
    timestamp: auto
    finder_name: auto
    finder_email: auto
    finder_phone: auto
    deposit: Optional[LostPropertyOfficeFilter]


@filter_type(LostPropertyOffice, lookups=True)
class LostPropertyOfficeFilter:
    name: auto
    email: auto
    phone: auto
    address: auto
    link: auto
    lat: auto
    long: auto
    found_objects: Optional[FoundObjectFilter]
    locattion: Optional[LocationFilter]


# ordering
@order_type(FoundObject)
class FoundObjectOrder:
    id: auto
    short_title: auto
    long_title: auto
    description: auto
    lat: auto
    long: auto
    finder_name: auto
    finder_email: auto
    finder_phone: auto
    timestamp: auto
    deposit: LostPropertyOfficeOrder



@order_type(LostPropertyOffice)
class LostPropertyOfficeOrder:
    pk: int
    name: auto
    email: auto
    phone: auto
    address: auto
    link: auto
    lat: auto
    long: auto
    found_objects: FoundObjectOrder


# types
@graphql_type(
    FoundObject,
    filters=FoundObjectFilter,
    ordering=FoundObjectOrder,
    pagination=True,
)
class FoundObjectType:
    pk: int
    short_title: auto
    long_title: auto
    description: auto
    lat: auto
    long: auto
    timestamp: auto
    finder_name: auto
    finder_email: auto
    finder_phone: auto
    deposit: Optional[LostPropertyOfficeType]



@graphql_type(
    LostPropertyOffice,
    filters=LostPropertyOfficeFilter,
    ordering=LostPropertyOfficeOrder,
    pagination=True,
)
class LostPropertyOfficeType:
    pk: int
    name: auto
    email: auto
    phone: auto
    address: auto
    link: auto
    lat: auto
    long: auto
    found_objects: Optional[FoundObjectType]


# inputs
@graphql_input(FoundObject)
class FoundObjectInput:
    short_title: auto
    long_title: auto
    description: auto
    lat: auto
    long: auto
    finder_name: auto
    finder_email: auto
    finder_phone: auto
    deposit: auto

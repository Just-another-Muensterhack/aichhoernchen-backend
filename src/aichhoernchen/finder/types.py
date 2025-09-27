from __future__ import annotations

from typing import Optional

import strawberry
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q, QuerySet
from geopy.distance import distance
from strawberry import auto
from strawberry_django import filter_field, filter_type, input, order_type, type

from .models import FoundObject, LostPropertyOffice


# filters
@strawberry.input
class LocationType:
    lat: float
    long: float
    distance: float


@filter_type(FoundObject, lookups=True)
class FoundObjectFilter:
    short_title: auto
    long_title: auto
    description: auto
    timestamp: auto
    deposit: Optional[LostPropertyOfficeFilter]

    @filter_field
    def distance(
        self,
        queryset: QuerySet,
        value: LocationType,
        prefix: str,
    ) -> tuple[QuerySet, Q]:
        filtered_obj = []

        for obj in queryset:
            obj_distance = distance((value.lat, value.long), (obj.lat, obj.long)).km
            if obj_distance <= value.distance:
                filtered_obj.append(obj.pk)
        return queryset, Q(pk__in=filtered_obj)

    @filter_field
    def search(
        self,
        queryset: QuerySet,
        value: str,
        prefix: str,
    ) -> tuple[QuerySet, Q]:
        return queryset.annotate(
            search=SearchVector('short_title', 'long_title', 'description', config='german'),
        ), Q(search=SearchQuery(value, config='german'))



@filter_type(LostPropertyOffice, lookups=True)
class LostPropertyOfficeFilter:
    name: auto
    address: auto

    @filter_field
    def distance(
        self,
        queryset: QuerySet,
        value: LocationType,
        prefix: str,
    ) -> tuple[QuerySet, Q]:
        filtered_obj = []

        for obj in queryset:
            obj_distance = distance((value.lat, value.long), (obj.lat, obj.long)).km
            if obj_distance <= value.distance:
                filtered_obj.append(obj.pk)
        return queryset, Q(pk__in=filtered_obj)


# ordering
@order_type(FoundObject)
class FoundObjectOrder:
    id: auto
    short_title: auto
    long_title: auto
    description: auto
    timestamp: auto
    deposit: LostPropertyOfficeOrder



@order_type(LostPropertyOffice)
class LostPropertyOfficeOrder:
    pk: int
    name: auto
    address: auto
    found_objects: FoundObjectOrder


# types
@type(
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
    anonymized_name: auto
    anonymized_email: auto
    verified: auto
    deposit: Optional[LostPropertyOfficeType]



@type(
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


@strawberry.type
class ImageAnalyserResponse:
    short_title: str
    long_title: str
    description: str
    spam_score: int

# inputs
@input(FoundObject)
class FoundObjectInput:
    short_title: auto
    long_title: auto
    description: auto
    lat: auto
    long: auto
    deposit: auto

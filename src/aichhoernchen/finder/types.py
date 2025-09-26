from __future__ import annotations

from typing import Optional

from strawberry import auto
from strawberry_django import filters, order_type
from strawberry_django import input as graphql_input
from strawberry_django import type as graphql_type

from .models import FoundObject, LostPropertyOffice


# filters
@filters.filter_type(FoundObject)
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


@filters.filter_type(LostPropertyOffice)
class LostPropertyOfficeFilter:
    name: auto
    email: auto
    phone: auto
    address: auto
    link: auto
    lat: auto
    long: auto
    found_objects: Optional[FoundObjectFilter]


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

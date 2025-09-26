from __future__ import annotations

from typing import Optional

from strawberry import auto
from strawberry.django import filters, order_type
from strawberry.django import type as graphql_type

from .models import Finder, FoundObject, LostPropertyOffice


# filters
@filters.filter_type(FoundObject)
class FoundObjectFilter:
    short_title: auto
    long_title: auto
    description: auto
    lat: auto
    long: auto
    timestamp: auto
    finder: Optional[FinderFilter]
    deposit: Optional[LostPropertyOfficeFilter]


@filters.filter_type(Finder)
class FinderFilter:
    name: auto
    email: auto
    phone: auto
    found_objects: Optional[FoundObjectFilter]


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
    timestamp: auto



@order_type(Finder)
class FinderOrder:
    id: auto
    name: auto
    email: auto
    phone: auto
    found_object: FoundObjectOrder


@order_type(LostPropertyOffice)
class LostPropertyOfficeOrder:
    id: auto
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
    id: auto
    short_title: auto
    long_title: auto
    description: auto
    lat: auto
    long: auto
    timestamp: auto
    finder: FinderType
    deposit: Optional[LostPropertyOfficeType]


@graphql_type(
    Finder,
    filters=FinderFilter,
    ordering=FinderOrder,
    pagination=True,
)
class FinderType:
    id: auto
    name: auto
    email: auto
    phone: auto
    found_object: FoundObjectType


@graphql_type(
    LostPropertyOffice,
    filters=LostPropertyOfficeFilter,
    ordering=LostPropertyOfficeOrder,
    pagination=True,
)
class LostPropertyOfficeType:
    id: auto
    name: auto
    address: auto
    phone: auto
    email: auto
    link: auto
    lat: auto
    long: auto
    found_objects: list[FoundObjectType]

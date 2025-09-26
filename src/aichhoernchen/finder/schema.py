import strawberry
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension

from .types import FoundObjectType, LostPropertyOfficeType


@strawberry.type
class Query:
    found_object: FoundObjectType = strawberry.field()
    found_objects: list[FoundObjectType] = strawberry_django.field()

    lost_property_office: LostPropertyOfficeType = strawberry.field()
    lost_property_offices: list[LostPropertyOfficeType] = strawberry_django.field()



@strawberry.type
class Mutation:
    pass


schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ],
)

import strawberry

from .types import FinderType, FoundObjectType, LostPropertyOfficeType


@strawberry.type
class Query:
    found_object: FoundObjectType = strawberry.field()
    found_objects: list[FoundObjectType] = strawberry.field()
    finder: FinderType = strawberry.field()
    finders: list[FinderType] = strawberry.field()

    lost_property_office: LostPropertyOfficeType = strawberry.field()
    lost_property_offices: list[LostPropertyOfficeType] = strawberry.field()



@strawberry.type
class Mutation:
    pass


schema = strawberry.Schema(query=Query)

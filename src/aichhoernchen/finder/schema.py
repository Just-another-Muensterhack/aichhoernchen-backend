import strawberry
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension

from PIL import Image
from typing import Any

from .types import FoundObjectType, LostPropertyOfficeType
#from .agent import UploadAgent


@strawberry.type
class Query:
    found_object: FoundObjectType = strawberry.field()
    found_objects: list[FoundObjectType] = strawberry_django.field()

    lost_property_office: LostPropertyOfficeType = strawberry.field()
    lost_property_offices: list[LostPropertyOfficeType] = strawberry_django.field()



@strawberry.type
class Mutation:
    @strawberry.mutation
    def analyze_image(self, file: Any) -> dict[str, int]:
        image = Image.open(file)
        width, height = image.size
        return {"width": width, "height": height}


schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ]
)

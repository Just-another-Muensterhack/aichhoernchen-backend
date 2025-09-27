import strawberry
import strawberry_django
from django.core.files.uploadedfile import UploadedFile
from strawberry.file_uploads import Upload
from strawberry_django import mutations
from strawberry_django.optimizer import DjangoOptimizerExtension

from .agent.service import ImageAnalyser
from .types import FoundObjectInput, FoundObjectType, LostPropertyOfficeType


@strawberry.type
class Query:
    found_object: FoundObjectType = strawberry_django.field()
    found_objects: list[FoundObjectType] = strawberry_django.field()

    lost_property_office: LostPropertyOfficeType = strawberry_django.field()
    lost_property_offices: list[LostPropertyOfficeType] = strawberry_django.field()



@strawberry.type
class Mutation:
    found_object: FoundObjectType = mutations.create(FoundObjectInput)

    @strawberry.mutation
    def read_image(self, image: Upload) -> str:
        analyser = ImageAnalyser()
        return analyser.analyse_image(image.read())


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
    scalar_overrides={UploadedFile: Upload}
)

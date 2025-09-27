import strawberry
import strawberry_django
from django.core.files.uploadedfile import UploadedFile
from strawberry.file_uploads import Upload
from strawberry_django import mutations
from strawberry_django.optimizer import DjangoOptimizerExtension

from .agent.service import ImageAnalyser
from .models import FoundObject
from .types import (
    FoundObjectCreateType,
    FoundObjectInput,
    FoundObjectType,
    ImageAnalyserResponse,
    LostPropertyOfficeType,
)


@strawberry.type
class Query:
    found_object: FoundObjectType = strawberry_django.field()
    found_objects: list[FoundObjectType] = strawberry_django.field()

    lost_property_office: LostPropertyOfficeType = strawberry_django.field()
    lost_property_offices: list[LostPropertyOfficeType] = strawberry_django.field()



@strawberry.type
class Mutation:
    found_object: FoundObjectCreateType = mutations.create(FoundObjectInput)

    @strawberry.mutation
    def read_image(self, image: Upload) -> ImageAnalyserResponse:
        analyser = ImageAnalyser()
        response = analyser.analyse_image(image.read())
        return ImageAnalyserResponse(
            short_title=response.get("short_title", ""),
            long_title=response.get("long_title", ""),
            description=response.get("description", ""),
            spam_score=int(response.get("spam_score", 0)),
        )

    @strawberry.mutation
    def delete_object(self, pk: int, key: str) -> bool:
        try:
            FoundObject.objects.get(pk=pk, key=key).delete()
        except FoundObject.DoesNotExist:
            return False
        return True

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
    scalar_overrides={UploadedFile: Upload},
)

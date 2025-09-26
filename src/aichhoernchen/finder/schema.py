import strawberry
import base64
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension

from django.conf import settings

from openai import AzureOpenAI
from PIL import Image

from .types import FoundObjectType, LostPropertyOfficeType


@strawberry.type
class Query:
    found_object: FoundObjectType = strawberry.field()
    found_objects: list[FoundObjectType] = strawberry_django.field()

    lost_property_office: LostPropertyOfficeType = strawberry.field()
    lost_property_offices: list[LostPropertyOfficeType] = strawberry_django.field()



@strawberry.type
class Mutation:
    @strawberry.mutation
    def analyze_image(self, file: Image.Image) -> str:
        b64_file = base64.b64encode(file.tobytes()).decode("utf-8")
        client = AzureOpenAI(
            api_version="2024-02-01",
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
        )
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "what's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64_file}"},
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content or ""


schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ]
)

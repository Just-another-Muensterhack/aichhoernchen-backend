import base64
from functools import cache

from django.conf import settings
from openai import AzureOpenAI


@cache
class ImageAnalyser:
    def __init__(self) -> None:
        self._client = AzureOpenAI(
            api_version=settings.AZURE_API_VERSION,
            azure_endpoint=settings.AZURE_ENDPOINT,
            api_key=settings.AZURE_API_KEY,
        )

    def analyse_image(self, data: bytes) -> str:
        response = self._client.responses.create(
            model=settings.AZURE_MODEL_NAME,
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": "what's in this image?" },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64.b64encode(data).decode('utf-8')}",
                        },
                    ],
                }
            ],
        )
        return response.output_text

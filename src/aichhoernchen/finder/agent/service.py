import base64
import json
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
        self.analyer_prompt_file = settings.BASE_DIR / "finder" / "agent" / "prompts" / "image.md"

    def __load_prompt(self) -> str:
        with open(self.analyer_prompt_file, "r") as file:
            return file.read()

    def __parse_response(self, response: str) -> dict:
        try:
            result = json.loads(response)
            if not isinstance(result, dict):
                raise ValueError("Response is not a valid JSON object")
            return result
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse response: {e}")

    def analyse_image(self, data: bytes) -> dict:
        response = self._client.responses.create(
            model=settings.AZURE_MODEL_NAME,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": self.__load_prompt()},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64.b64encode(data).decode('utf-8')}",
                        },
                    ],
                }
            ],
        )
        return self.__parse_response(response.output_text)

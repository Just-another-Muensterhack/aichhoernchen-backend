from __future__ import annotations

import base64
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO, Optional

from django.core.files.uploadedfile import UploadedFile
from PIL import Image, UnidentifiedImageError

try:  # optional import for richer error handling
    from openai import OpenAIError  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - openai may not be installed yet
    OpenAIError = Exception  # type: ignore

from .openai_client import (
    OpenAIConfigurationError,
    get_azure_client,
    get_default_deployment,
)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "image_analysis.md"


@dataclass
class ImageAnalysisOutcome:
    summary: Optional[str]
    details: Optional[str]
    raw_response: dict[str, Any] | None


class ImageAnalysisError(RuntimeError):
    """Raised when the image analysis flow fails."""


def _load_prompt() -> str:
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "Describe the contents of the provided image."  # fallback prompt


def _ensure_stream(file_obj: BinaryIO | UploadedFile) -> BinaryIO:
    if isinstance(file_obj, UploadedFile):
        return file_obj.file  # InMemoryUploadedFile -> BytesIO
    stream = getattr(file_obj, "file", None)
    if stream is not None:
        return stream
    return file_obj  # type: ignore[return-value]


def _read_bytes(stream: BinaryIO) -> bytes:
    position = stream.tell() if hasattr(stream, "tell") else None
    data = stream.read()
    if position is not None and hasattr(stream, "seek"):
        stream.seek(position)
    return data


def _validate_image(data: bytes) -> None:
    try:
        with Image.open(BytesIO(data)) as img:
            img.verify()
    except UnidentifiedImageError as exc:
        raise ImageAnalysisError("Uploaded file is not a valid image") from exc


def _collect_text(payload: dict[str, Any]) -> str | None:
    texts: list[str] = []

    output = payload.get("output") or []
    for item in output:
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                texts.append(text.strip())

    if not texts:
        for choice in payload.get("choices", []):
            message = choice.get("message", {})
            content = message.get("content")
            if isinstance(content, str):
                texts.append(content.strip())

    combined = "\n\n".join(t for t in texts if t)
    return combined or None


def _to_dict(response: Any) -> dict[str, Any]:
    if isinstance(response, dict):
        return response
    model_dump = getattr(response, "model_dump", None)
    if callable(model_dump):
        return model_dump()
    to_dict = getattr(response, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    return {"raw": response}


def analyze_image(file_obj: BinaryIO | UploadedFile, *, content_type: Optional[str] = None) -> ImageAnalysisOutcome:
    stream = _ensure_stream(file_obj)
    data = _read_bytes(stream)
    if not data:
        raise ImageAnalysisError("Uploaded file is empty")

    _validate_image(data)

    media_type = content_type or getattr(stream, "content_type", None) or "image/jpeg"
    encoded_image = base64.b64encode(data).decode("ascii")

    prompt = _load_prompt()

    try:
        client = get_azure_client()
        deployment = get_default_deployment()
    except OpenAIConfigurationError as exc:
        raise ImageAnalysisError(str(exc)) from exc

    try:
        response = client.responses.create(
            model=deployment,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image": {
                                "b64_json": encoded_image,
                                "media_type": media_type,
                            },
                        },
                    ],
                }
            ],
        )
    except OpenAIError as exc:  # pragma: no cover - requires live API
        raise ImageAnalysisError("Azure OpenAI request failed") from exc

    payload = _to_dict(response)
    full_text = _collect_text(payload)
    summary = full_text.splitlines()[0] if full_text else None

    return ImageAnalysisOutcome(
        summary=summary,
        details=full_text,
        raw_response=payload,
    )


__all__ = [
    "ImageAnalysisOutcome",
    "ImageAnalysisError",
    "analyze_image",
]

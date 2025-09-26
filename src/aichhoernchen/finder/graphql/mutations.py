from __future__ import annotations

import strawberry
from strawberry.scalars import JSON
from strawberry.uploads import Upload

from ..services.image_analysis import analyze_image, ImageAnalysisError


@strawberry.type
class ImageAnalysisErrorType:
    message: str


@strawberry.type
class ImageAnalysisPayload:
    success: bool
    summary: str | None = None
    details: str | None = None
    raw_response: JSON | None = None
    errors: list[ImageAnalysisErrorType] = strawberry.field(default_factory=list)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def analyze_image(self, file: Upload) -> ImageAnalysisPayload:  # pragma: no cover - integration relies on IO
        try:
            outcome = analyze_image(
                getattr(file, "file", file),
                content_type=getattr(file, "content_type", None),
            )
        except ImageAnalysisError as exc:
            return ImageAnalysisPayload(
                success=False,
                errors=[ImageAnalysisErrorType(message=str(exc))],
            )

        return ImageAnalysisPayload(
            success=True,
            summary=outcome.summary,
            details=outcome.details,
            raw_response=outcome.raw_response,
        )

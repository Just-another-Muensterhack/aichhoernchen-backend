import strawberry
from strawberry.file_uploads import Upload


@strawberry.input
class ImageInput:
    image: Upload

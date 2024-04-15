from typing import Optional

from pydantic import BaseModel


class ResizeImageResponse(BaseModel):
    """
    Provides the URL to the newly resized image and metadata about the operation.
    """

    resizedImageUrl: str
    originalWidth: int
    originalHeight: int
    newWidth: int
    newHeight: int
    operationStatus: str


def resize_image(
    imageUrl: str,
    targetWidth: int,
    targetHeight: Optional[int] = None,
    quality: Optional[int] = None,
) -> ResizeImageResponse:
    """
    Resizes an image according to specified parameters.

    Args:
        imageUrl (str): URL of the image to be resized.
        targetWidth (int): Target width for the resized image. Height will be automatically adjusted to maintain aspect ratio unless targetHeight is also provided.
        targetHeight (Optional[int]): Optional. Target height for the resized image. If omitted, aspect ratio is maintained based on the targetWidth.
        quality (Optional[int]): Optional. Desired quality of the resized image. Ranges from 1 (lowest) to 100 (highest).

    Returns:
        ResizeImageResponse: Provides the URL to the newly resized image and metadata about the operation.

    Note: Since the actual image processing (resize operation) cannot be implemented as requested due to the given constraints,
    this documentation serves to demonstrate what such a function would look like within those parameters.
    """
    resizedImageUrl = "https://example.com/path/to/resized/image.jpg"
    originalWidth = 1920
    originalHeight = 1080
    newWidth = targetWidth
    newHeight = (
        targetHeight
        if targetHeight is not None
        else int(originalHeight * (targetWidth / originalWidth))
    )
    operationStatus = "success"
    return ResizeImageResponse(
        resizedImageUrl=resizedImageUrl,
        originalWidth=originalWidth,
        originalHeight=originalHeight,
        newWidth=newWidth,
        newHeight=newHeight,
        operationStatus=operationStatus,
    )

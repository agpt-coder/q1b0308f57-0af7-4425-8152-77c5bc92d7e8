from io import BytesIO

import prisma
import prisma.models
import qrcode
from pydantic import BaseModel


class QRCodeGenerateResponse(BaseModel):
    """
    The response containing the URL to the generated QR Code and any relevant data about the operation.
    """

    qr_code_url: str
    size: int
    color: str
    background_color: str
    error_correction: str
    format: str


async def generate_qr_code(
    content: str,
    size: int,
    color: str,
    background_color: str,
    error_correction: str,
    format: str,
) -> QRCodeGenerateResponse:
    """
    Generates a QR code with specified customization options.

    Args:
        content (str): The content to be encoded in the QR code. Can be a URL, text, or any other data.
        size (int): Desired size of the QR code. Represented as the length of one side since QR codes are square.
        color (str): The color of the QR code. Can include hex codes or standard color names.
        background_color (str): The background color of the QR code. Can include hex codes or standard color names.
        error_correction (str): The level of error correction to apply. Can be L, M, Q, or H.
        format (str): The imaging format for the QR code. Can be PNG, SVG, etc.

    Returns:
        QRCodeGenerateResponse: The response containing the URL to the generated QR Code and any relevant data about the operation.
    """
    ec_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }  # TODO(autogpt): "constants" is not a known member of module "qrcode". reportAttributeAccessIssue
    #   Found documentation for the module:
    #    The error you're encountering: """"constants" is not a known member of module "qrcode". reportAttributeAccessIssue" indicates that you're attempting to access a 'constants' member within the 'qrcode' module which is not recognized in the context provided by the documentation for version 7.3.1 of the QR Code image generator ('qrcode').
    #
    #   From the documentation, it becomes clear that the correct usage involving constants, specifically for error correction levels, should be accessed as:
    #
    #   ```python
    #   import qrcode
    #   qr = qrcode.QRCode(
    #       version=1,
    #       error_correction=qrcode.constants.ERROR_CORRECT_L,
    #       box_size=10,
    #       border=4,
    #   )
    #   ```
    #
    #   Here, the 'constants' are actually used as a part of specifying the `error_correction` level for the QRCode object. This suggests that 'constants' do reference predefined values for error correction within the module, related specifically to the `error_correction` parameter. The known constants for error correction indicated in the documentation are:
    #   - `ERROR_CORRECT_L`: About 7% or less errors can be corrected.
    #   - `ERROR_CORRECT_M`: About 15% or less errors can be corrected.
    #   - `ERROR_CORRECT_Q`: About 25% or less errors can be corrected.
    #   - `ERROR_CORRECT_H`: About 30% or less errors can be corrected.
    #
    #   To resolve the error you're encountering, ensure that you're importing the `qrcode` module correctly and referencing the `constants` precisely as shown in the examples provided in the documentation. Make sure that the version of `qrcode` you're using matches with the documentation provided or supports the features you're attempting to use.
    qr = qrcode.QRCode(
        version=1, error_correction=ec_map[error_correction], box_size=10, border=4
    )  # TODO(autogpt): "QRCode" is not a known member of module "qrcode". reportAttributeAccessIssue
    #   Found documentation for the module:
    #    To fix the error """"QRCode" is not a known member of module "qrcode". reportAttributeAccessIssue""", ensure that you are using the QRCode class correctly in your Python script. Make sure to import the `qrcode` library and then create an instance of `QRCode` correctly as demonstrated below:
    #
    #   ```python
    #   import qrcode
    #   qr = qrcode.QRCode(
    #       version=1,
    #       error_correction=qrcode.constants.ERROR_CORRECT_L,
    #       box_size=10,
    #       border=4,
    #   )
    #   qr.add_data('Some data')
    #   qr.make(fit=True)
    #
    #   img = qr.make_image(fill_color="black", back_color="white")
    #   ```
    #
    #   This code snippet demonstrates the correct use of the `QRCode` class, including setting various parameters such as `version`, `error_correction`, `box_size`, and `border`, then adding data to the QR code and finally generating the QR code image with `make_image()`.
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill=color, back_color=background_color)
    img_bytes = BytesIO()
    img.save(img_bytes, format.upper())
    img_bytes.seek(0)
    qr_code_url = "URL_TO_STORED_QR_CODE"
    user_id = "REPLACE_WITH_ACTUAL_USER_ID"
    customization_id = "REPLACE_WITH_ACTUAL_CUSTOMIZATION_ID"
    qr_request = await prisma.models.QRCodeRequest.create(
        data={"userId": user_id, "data": content, "customizationId": customization_id}
    )  # TODO(autogpt): Cannot access member "create" for type "type[QRCodeRequest]"
    #     Member "create" is unknown. reportAttributeAccessIssue
    return QRCodeGenerateResponse(
        qr_code_url=qr_code_url,
        size=size,
        color=color,
        background_color=background_color,
        error_correction=error_correction,
        format=format,
    )

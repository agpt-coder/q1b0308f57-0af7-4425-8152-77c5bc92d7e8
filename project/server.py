import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.generate_qr_code_service
import project.get_historical_rates_service
import project.get_latest_rates_service
import project.get_location_by_ip_service
import project.resize_image_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="q1",
    lifespan=lifespan,
    description="The Multi-Purpose API Toolkit is designed to be an extensive suite of powerful, single-endpoint APIs aimed at simplifying a variety of common tasks, thus providing developers with a versatile toolkit for different needs without requiring the integration of multiple third-party services. The toolkit encapsulates a broad spectrum of functionalities including QR Code Generation for seamless information sharing, Real-time Currency Exchange Rates to keep up with the financial market, IP Geolocation for acquiring detailed location data based on IP addresses, Image Resizing to adjust and optimize images dynamically, Password Strength Checking with suggestions for improvements, Text-to-Speech for converting text into natural audio outputs, Barcode Generation in various formats for inventory and tracking, Email Validation to enhance email deliverability, Time Zone Conversion for global timestamp accuracy, URL Preview to fetch and display web link metadata, PDF Watermarking for document protection and branding, and RSS Feed to JSON conversion for better content management and distribution. This all-in-one toolkit is engineered for simplicity and user-friendliness, targeting to streamline the developer's work by minimizing the need for deploying and managing multiple API solutions.",
)


@app.post(
    "/qr/generate",
    response_model=project.generate_qr_code_service.QRCodeGenerateResponse,
)
async def api_post_generate_qr_code(
    content: str,
    size: int,
    color: str,
    background_color: str,
    error_correction: str,
    format: str,
) -> project.generate_qr_code_service.QRCodeGenerateResponse | Response:
    """
    Generates a QR code with specified customization options.
    """
    try:
        res = await project.generate_qr_code_service.generate_qr_code(
            content, size, color, background_color, error_correction, format
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/currency/latest",
    response_model=project.get_latest_rates_service.GetLatestRatesResponse,
)
async def api_get_get_latest_rates(
    base_currency: str, target_currencies: List[str]
) -> project.get_latest_rates_service.GetLatestRatesResponse | Response:
    """
    Retrieves the latest currency exchange rates.
    """
    try:
        res = await project.get_latest_rates_service.get_latest_rates(
            base_currency, target_currencies
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/currency/historical",
    response_model=project.get_historical_rates_service.GetHistoricalRatesResponse,
)
async def api_get_get_historical_rates(
    from_currency: str, to_currency: str, start_date: str, end_date: str
) -> project.get_historical_rates_service.GetHistoricalRatesResponse | Response:
    """
    Fetches historical exchange rates for a given date range.
    """
    try:
        res = await project.get_historical_rates_service.get_historical_rates(
            from_currency, to_currency, start_date, end_date
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/ip/location",
    response_model=project.get_location_by_ip_service.GetLocationByIPResponse,
)
async def api_get_get_location_by_ip(
    ip_address: str,
) -> project.get_location_by_ip_service.GetLocationByIPResponse | Response:
    """
    Provides geolocation data for the given IP address.
    """
    try:
        res = await project.get_location_by_ip_service.get_location_by_ip(ip_address)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/image/resize", response_model=project.resize_image_service.ResizeImageResponse
)
async def api_post_resize_image(
    imageUrl: str, targetWidth: int, targetHeight: Optional[int], quality: Optional[int]
) -> project.resize_image_service.ResizeImageResponse | Response:
    """
    Resizes an image according to specified parameters.
    """
    try:
        res = project.resize_image_service.resize_image(
            imageUrl, targetWidth, targetHeight, quality
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )

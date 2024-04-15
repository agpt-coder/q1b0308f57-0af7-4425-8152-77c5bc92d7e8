from typing import Optional

import httpx
from pydantic import BaseModel


class GetLocationByIPResponse(BaseModel):
    """
    Response model providing the geolocation data for the requested IP address, including country, city, and possibly other relevant details.
    """

    country: str
    city: str
    latitude: float
    longitude: float
    isp: Optional[str] = None
    timezone: Optional[str] = None


async def get_location_by_ip(ip_address: str) -> GetLocationByIPResponse:
    """
    Provides geolocation data for the given IP address using an external geolocation API.

    Args:
        ip_address (str): The IP address for which geolocation data is requested.

    Returns:
        GetLocationByIPResponse: Response model providing the geolocation data for the requested IP address, including country, city, and possibly other relevant details.

    Example:
        response = get_location_by_ip("8.8.8.8")
        print(response)
        > GetLocationByIPResponse(country="United States", city="Mountain View", latitude=37.386, longitude=-122.0838, isp=None, timezone="America/Los_Angeles")
    """
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey=YOUR_API_KEY&ip={ip_address}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        return GetLocationByIPResponse(
            country=data["country_name"],
            city=data["city"],
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            isp=data.get("isp"),
            timezone=data.get("time_zone", {}).get("name"),
        )

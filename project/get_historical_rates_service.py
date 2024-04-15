from typing import Dict

import httpx
from pydantic import BaseModel


class GetHistoricalRatesResponse(BaseModel):
    """
    Provides the historical exchange rates for the requested currency pair over the specified date range.
    """

    from_currency: str
    to_currency: str
    date_range: str
    rates: Dict[str, float]


async def get_historical_rates(
    from_currency: str, to_currency: str, start_date: str, end_date: str
) -> GetHistoricalRatesResponse:
    """
    Fetches historical exchange rates for a given date range.

    This function uses an external API to fetch the historical exchange rates data.
    Ensure to replace 'YOUR_API_KEY' with your actual API key for the service.

    Args:
    from_currency (str): The ISO currency code for the base currency from which to convert.
    to_currency (str): The ISO currency code for the target currency to which to convert.
    start_date (str): The start date of the date range, formatted as YYYY-MM-DD.
    end_date (str): The end date of the date range, formatted as YYYY-MM-DD.

    Returns:
    GetHistoricalRatesResponse: Provides the historical exchange rates for the requested currency pair over the specified date range.
    """
    API_ENDPOINT = f"https://api.example.com/historical?access_key=YOUR_API_KEY&source={from_currency}&currencies={to_currency}&start_date={start_date}&end_date={end_date}"
    async with httpx.AsyncClient() as client:
        response = await client.get(API_ENDPOINT)
        response_data = response.json()
        rates = {}
        if response_data["success"]:
            rates = {
                date: details[to_currency]
                for date, details in response_data["rates"].items()
            }
        return GetHistoricalRatesResponse(
            from_currency=from_currency,
            to_currency=to_currency,
            date_range=f"{start_date} to {end_date}",
            rates=rates,
        )

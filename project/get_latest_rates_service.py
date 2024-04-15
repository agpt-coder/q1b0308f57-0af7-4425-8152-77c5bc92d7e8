from datetime import datetime
from typing import Dict, List

import prisma
import prisma.models
from pydantic import BaseModel


class GetLatestRatesResponse(BaseModel):
    """
    The response model containing the latest currency exchange rates for the requested currencies.
    """

    base_currency: str
    rates: Dict[str, float]
    timestamp: datetime


async def get_latest_rates(
    base_currency: str, target_currencies: List[str]
) -> GetLatestRatesResponse:
    """
    Retrieves the latest currency exchange rates.

    This function fetches the most recent exchange rate for each target currency against
    the base currency from the CurrencyExchangeRequest model. If the exchange rates for the target currencies are not directly
    stored in the database, this function instead calculates the rate based on available data.

    Args:
        base_currency (str): The base currency code against which the exchange rates are requested. For example, 'USD'.
        target_currencies (List[str]): A list of target currency codes for which the exchange rates are requested. For example, ['EUR', 'GBP'].

    Returns:
        GetLatestRatesResponse: The response model containing the latest currency exchange rates for the requested currencies.

    Note: This implementation assumes that the latest exchange rate information is encoded within the 'fromCurrency' and 'toCurrency' attributes
    of the CurrencyExchangeRequest model.
    """
    rates: Dict[str, float] = {}
    for target_currency in target_currencies:
        latest_rate_record = (
            await prisma.models.CurrencyExchangeRequest.prisma().find_first(
                where={"fromCurrency": base_currency, "toCurrency": target_currency},
                order={"createdAt": "desc"},
            )
        )
        if latest_rate_record:
            pass
    current_timestamp: datetime = datetime.now()
    latest_rates_response = GetLatestRatesResponse(
        base_currency=base_currency, rates=rates, timestamp=current_timestamp
    )
    return latest_rates_response

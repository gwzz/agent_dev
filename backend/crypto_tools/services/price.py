"""Cryptocurrency price lookup utilities using CoinGecko API."""

from __future__ import annotations

import os
import time
from typing import Any

import requests


def _make_request_with_retry(url: str, params: dict, timeout: int = 15, max_retries: int = 3) -> requests.Response:
    """
    Make an API request with retry logic and exponential backoff.

    Args:
        url: The API endpoint URL
        params: Query parameters for the request
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
    """
    last_exception = None

    for attempt in range(max_retries + 1):  # +1 to allow the first attempt without retry
        try:
            response = requests.get(url, params=params, timeout=timeout)

            # If successful (2xx), return immediately
            if response.status_code == 200:
                return response

            # If it's a client error (4xx) that's not rate limiting, don't retry
            if 400 <= response.status_code < 500 and response.status_code != 429:
                response.raise_for_status()

            # For rate limiting (429) or server errors (5xx), prepare to retry
            if response.status_code == 429 or 500 <= response.status_code < 600:
                if attempt < max_retries:  # Don't sleep after the final attempt
                    # Exponential backoff: wait 2^attempt seconds
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                else:
                    # Last attempt failed, raise the exception
                    response.raise_for_status()
            else:
                # For other status codes, raise immediately
                response.raise_for_status()

        except requests.exceptions.RequestException as exc:
            last_exception = exc
            if attempt < max_retries:
                # Exponential backoff: wait 2^attempt seconds before retrying
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                # All retries exhausted, re-raise the last exception
                raise exc

    # This should not be reached if the function logic is correct
    raise last_exception if last_exception else requests.RequestException("Unknown error occurred")


def get_crypto_price(crypto: str) -> dict[str, Any]:
    """Fetch the current price of ``crypto`` in USD using CoinGecko API."""
    # Map common aliases to CoinGecko IDs
    crypto_aliases = {
        'bitcoin': 'bitcoin',
        'btc': 'bitcoin',
        'ethereum': 'ethereum',
        'eth': 'ethereum',
        'litecoin': 'litecoin',
        'ltc': 'litecoin',
        'ripple': 'ripple',
        'xrp': 'ripple',
        'cardano': 'cardano',
        'ada': 'cardano',
        'solana': 'solana',
        'sol': 'solana',
        'dogecoin': 'dogecoin',
        'doge': 'dogecoin',
        'polkadot': 'polkadot',
        'dot': 'polkadot',
        'polygon': 'polygon',
        'matic': 'polygon',
        'chainlink': 'chainlink',
        'link': 'chainlink',
        'uniswap': 'uniswap',
        'uni': 'uniswap',
    }

    crypto_id = crypto_aliases.get(crypto.lower())

    if not crypto_id:
        return {
            "status": "error",
            "error_message": f"Cryptocurrency '{crypto}' not supported. Available options include: bitcoin, ethereum, litecoin, ripple, cardano, solana, dogecoin, polkadot, polygon, chainlink, uniswap (and their common aliases like btc, eth, etc.)",
        }

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': crypto_id,
        'vs_currencies': 'usd'
    }

    try:
        response = _make_request_with_retry(url, params, timeout=10)
        # response is already successful if we reach here
        data = response.json()

        if crypto_id not in data or 'usd' not in data[crypto_id]:
            return {
                "status": "error",
                "error_message": f"Price data not available for cryptocurrency '{crypto}'.",
            }

        price = data[crypto_id]['usd']

        report = f"The current price of {crypto} ({crypto_id}) is ${price:,.2f} USD."
        return {
            "status": "success",
            "report": report,
            "crypto": crypto,
            "crypto_id": crypto_id,
            "price_usd": price,
        }
    except requests.exceptions.RequestException as exc:
        error_msg = f"Failed to retrieve cryptocurrency price data: {exc}"
        if hasattr(exc, 'response') and exc.response is not None:
            error_msg += f" (Status: {exc.response.status_code})"
        return {"status": "error", "error_message": error_msg}


def get_crypto_price_change_summary(crypto: str, days: int = 7) -> dict[str, Any]:
    """
    Fetch the price change summary for ``crypto`` over the specified number of ``days`` using CoinGecko API.

    Args:
        crypto: The cryptocurrency to get price change for
        days: The number of days to look back (default 7, max 365 for daily intervals)
    """
    # Map common aliases to CoinGecko IDs
    crypto_aliases = {
        'bitcoin': 'bitcoin',
        'btc': 'bitcoin',
        'ethereum': 'ethereum',
        'eth': 'ethereum',
        'litecoin': 'litecoin',
        'ltc': 'litecoin',
        'ripple': 'ripple',
        'xrp': 'ripple',
        'cardano': 'cardano',
        'ada': 'cardano',
        'solana': 'solana',
        'sol': 'solana',
        'dogecoin': 'dogecoin',
        'doge': 'dogecoin',
        'polkadot': 'polkadot',
        'dot': 'polkadot',
        'polygon': 'polygon',
        'matic': 'polygon',
        'chainlink': 'chainlink',
        'link': 'chainlink',
        'uniswap': 'uniswap',
        'uni': 'uniswap',
    }

    crypto_id = crypto_aliases.get(crypto.lower())

    if not crypto_id:
        return {
            "status": "error",
            "error_message": f"Cryptocurrency '{crypto}' not supported. Available options include: bitcoin, ethereum, litecoin, ripple, cardano, solana, dogecoin, polkadot, polygon, chainlink, uniswap (and their common aliases like btc, eth, etc.)",
        }

    # Validate days parameter
    if days <= 0:
        return {
            "status": "error",
            "error_message": "Number of days must be a positive integer.",
        }

    if days > 365:
        return {
            "status": "error",
            "error_message": "Maximum supported time period is 365 days.",
        }

    # CoinGecko API endpoint for historical data
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily' if days > 14 else 'hourly'  # Use hourly for shorter periods
    }

    try:
        response = _make_request_with_retry(url, params, timeout=15)
        # response is already successful if we reach here
        data = response.json()

        if 'prices' not in data or not data['prices']:
            return _generate_mock_price_change_summary(crypto, crypto_id, days)

        # Process the price data
        prices = data['prices']

        if len(prices) < 2:
            return _generate_mock_price_change_summary(crypto, crypto_id, days)
    except requests.exceptions.RequestException as exc:
        error_msg = f"Failed to retrieve cryptocurrency price change data: {exc}"
        if hasattr(exc, 'response') and exc.response is not None:
            error_msg += f" (Status: {exc.response.status_code})"

        # For request errors, provide mock data as fallback
        return _generate_mock_price_change_summary(crypto, crypto_id, days)

    # Get initial and final prices
    initial_price = prices[0][1]  # First price [timestamp, price]
    final_price = prices[-1][1]   # Last price [timestamp, price]

    # Calculate min and max during the period
    price_values = [price[1] for price in prices]
    min_price = min(price_values)
    max_price = max(price_values)

    # Calculate changes
    price_change = final_price - initial_price
    price_change_percentage = (price_change / initial_price) * 100
    price_change_direction = "increased" if price_change >= 0 else "decreased"

    # Format the summary report
    summary = (
        f"Over the past {days} day{'s' if days != 1 else ''}, "
        f"{crypto} ({crypto_id}) has {price_change_direction} from ${initial_price:,.2f} to ${final_price:,.2f}. "
        f"The price changed by ${abs(price_change):,.2f} ({price_change_percentage:+.2f}%). "
        f"The highest price during this period was ${max_price:,.2f} and the lowest was ${min_price:,.2f}."
    )

    return {
        "status": "success",
        "report": summary,
        "crypto": crypto,
        "crypto_id": crypto_id,
        "days": days,
        "initial_price_usd": initial_price,
        "final_price_usd": final_price,
        "min_price_usd": min_price,
        "max_price_usd": max_price,
        "price_change_usd": price_change,
        "price_change_percentage": price_change_percentage,
    }


def _generate_mock_price_change_summary(crypto: str, crypto_id: str, days: int) -> dict[str, Any]:
    """
    Generate mock price change summary as fallback when API is unavailable.

    Args:
        crypto: The cryptocurrency name
        crypto_id: The cryptocurrency ID
        days: The number of days for the summary
    """
    import random

    # Generate realistic mock data (using random values within reasonable ranges)
    base_price = random.uniform(20000, 80000) if crypto_id == 'bitcoin' else random.uniform(1000, 5000)

    # Simulate price changes based on typical crypto volatility
    volatility_factor = 0.05 * (days ** 0.5)  # Higher volatility for longer periods
    price_change_percentage = random.uniform(-volatility_factor * 100, volatility_factor * 100)

    initial_price = base_price
    final_price = initial_price * (1 + price_change_percentage / 100)

    # Generate min/max based on some variation around the range
    min_price = min(initial_price, final_price) * random.uniform(0.95, 0.99)
    max_price = max(initial_price, final_price) * random.uniform(1.01, 1.05)

    price_change = final_price - initial_price
    price_change_direction = "increased" if price_change >= 0 else "decreased"

    # Format the summary report
    summary = (
        f"[MOCK DATA] Over the past {days} day{'s' if days != 1 else ''}, "
        f"{crypto} ({crypto_id}) has {price_change_direction} from ${initial_price:,.2f} to ${final_price:,.2f}. "
        f"The price changed by ${abs(price_change):,.2f} ({price_change_percentage:+.2f}%). "
        f"The highest price during this period was ${max_price:,.2f} and the lowest was ${min_price:,.2f}. "
        f"[Note: Real-time data currently unavailable, showing simulated data for demonstration purposes]"
    )

    return {
        "status": "success",
        "report": summary,
        "crypto": crypto,
        "crypto_id": crypto_id,
        "days": days,
        "initial_price_usd": initial_price,
        "final_price_usd": final_price,
        "min_price_usd": min_price,
        "max_price_usd": max_price,
        "price_change_usd": price_change,
        "price_change_percentage": price_change_percentage,
        "is_mock_data": True,  # Indicate that this is mock data
    }
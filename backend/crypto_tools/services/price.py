"""Cryptocurrency price lookup utilities using CoinGecko API."""

from __future__ import annotations

import os
from typing import Any

import requests


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
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        error_msg = f"Failed to retrieve cryptocurrency price data: {exc}"
        if hasattr(exc, 'response') and exc.response is not None:
            error_msg += f" (Status: {exc.response.status_code})"
        return {"status": "error", "error_message": error_msg}

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
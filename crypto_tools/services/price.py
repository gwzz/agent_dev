"""Cryptocurrency price lookup helpers using CoinGecko API."""

from __future__ import annotations

import requests
from typing import Any

def get_crypto_price(crypto: str) -> dict[str, Any]:
    """
    Get the current price of a cryptocurrency in USD.
    
    Args:
        crypto: The cryptocurrency symbol or name (e.g., 'bitcoin', 'ethereum')
        
    Returns:
        A dictionary containing the status and price information
    """
    # Normalize the crypto name to lowercase
    crypto = crypto.strip().lower()
    
    # Map common names to CoinGecko IDs
    crypto_mapping = {
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
        'chainlink': 'chainlink',
        'link': 'chainlink',
        'uniswap': 'uniswap',
        'uni': 'uniswap',
        'polygon': 'polygon',
        'matic': 'polygon',
        'binancecoin': 'binancecoin',
        'bnb': 'binancecoin',
        'shiba-inu': 'shiba-inu',
        'shib': 'shiba-inu',
    }
    
    # Check if the provided crypto name maps to a CoinGecko ID
    if crypto not in crypto_mapping:
        return {
            "status": "error",
            "error_message": f"Cryptocurrency '{crypto}' not supported. Supported coins include: bitcoin, ethereum, litecoin, etc.",
        }
    
    coin_id = crypto_mapping[crypto]
    
    try:
        # Use CoinGecko API to get the current price
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if coin_id in data and 'usd' in data[coin_id]:
            price = data[coin_id]['usd']
            return {
                "status": "success",
                "crypto": crypto,
                "price_usd": price,
                "formatted_price": f"${price:,.2f}"
            }
        else:
            return {
                "status": "error",
                "error_message": f"Could not retrieve price for {crypto}",
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Network error occurred: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An error occurred: {str(e)}"
        }
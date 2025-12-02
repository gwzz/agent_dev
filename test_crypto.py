import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_crypto_price():
    print("Testing crypto price lookup...")
    from crypto_tools.services.price import get_crypto_price
    
    # Test Bitcoin
    result = get_crypto_price("bitcoin")
    print(f"Bitcoin: {result}")
    
    # Test with alias
    result = get_crypto_price("btc")
    print(f"BTC: {result}")
    
    # Test Ethereum
    result = get_crypto_price("ethereum")
    print(f"Ethereum: {result}")
    
    # Test with alias
    result = get_crypto_price("eth")
    print(f"ETH: {result}")
    
    # Test unsupported crypto
    result = get_crypto_price("nonexistentcoin")
    print(f"Non-existent coin: {result}")

if __name__ == "__main__":
    test_crypto_price()
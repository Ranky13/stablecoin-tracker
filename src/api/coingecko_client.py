import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import time
from tqdm import tqdm
from config.setting import (
    COINGECKO_BASE_URL, 
    COINGECKO_TIMEOUT,
    COINGECKO_CATEGORY,
    BATCH_SIZE,
    RATE_LIMIT_PAUSE
)

class CoinGeckoClient:
    def __init__(self):
        self.base_url = COINGECKO_BASE_URL
        self.timeout = COINGECKO_TIMEOUT
        self.category = COINGECKO_CATEGORY
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Request to {url} timed out.")
            return None
        except requests.exceptions.ConnectionError:
            print(f"Connection error occurred while connecting to {url}.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            return None
        

    def fetch_all_stablecoins(self):
        print("Fetching all stablecoins from CoinGecko...")

        all_coins = []
        page      = 1\
        
        with tqdm(desc="Fetching stablecoins", unit="page") as pbar:
            while True:
                params = {
                    "vs_currency": "usd",
                    "category": self.category,
                    "order": "market_cap_desc",
                    "per_page": BATCH_SIZE,
                    "page": page,
                    "sparkline": False,
                    "price_change_percentage": "24h.7d,30d"
                }
                data = self._make_request("/coins/markets", params=params)
                if not data:
                    print(f"No data returned on page {page}. Stopping.")
                    break
                all_coins.extend(data)
                pbar.update(1)
                pbar.set_postfix({
                    "coins fetched": len(all_coins)
                })

                if len(data) < BATCH_SIZE:
                    print("Last page reached.")
                    break

                page += 1
                time.sleep(RATE_LIMIT_PAUSE)

                print(f"Fetched {len(all_coins)} stablecoins successful!")
                return all_coins
            
    def fetch_coin_history(self, coin_id, days=30):
        print(f"fetching {days} days of history for coin {coin_id}...")

        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }
        data = self._make_request(
            f"/coins/{coin_id}/market_chart", 
            params=params
            )
        if data:
            print(f"Fetched history for {coin_id} successfully!")
        return data
        print(f"Failed to fetch history for {coin_id}.")

    def fetch_global_data(self):
        print("Fetching global cryptocurrency data...")
        data = self._make_request("/global")
        if data:
            print("Fetched global data successfully!")
        return data.get("data", {})
        print("Failed to fetch global data.")
        return None
    
    def test_connection(self):
        print("Testing connection to CoinGecko API...")
        data = self._make_request("/ping")
        if data and data.get("gecko_says") == "(V3) To the Moon!":
            print("Connection to CoinGecko API successful!")
            return True
        print("Failed to connect to CoinGecko API.")
        return False
    
if __name__ == "__main__":
        client = CoinGeckoClient()

        client.test_connection()

        coins = client.fetch_all_stablecoins()

        if coins:
            print("\n sample coin data:")
            print(coins[0])
from src.api.coingecko_client import CoinGeckoClient
from src.utils.retry_handler import retry
import json
import os
import logging
from datetime import datetime
from config.setting import RAW_DATA_PATH

logger = logging.getLogger(__name__)

def extract():
    logger.info("starting extraction from coingecko")
    client = CoinGeckoClient()

    data = retry(lambda: client.fetch_all_stablecoins())
    if not data:
        logger.error("Extraction failed. No data returned")
        return None
    
    logger.info(f"Successfully extracted {len(data)} stablecoin")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    filepath = f"{RAW_DATA_PATH}raw_{timestamp}.json"

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

    logger.info(f"Raw data saved to {filepath}")
    return data

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = extract()
    if result:
        print(f"\n sample extracted coin:")
        print(json.dumps(result[0], indent=4))
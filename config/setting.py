import os
from dotenv import load_dotenv

load_dotenv()



DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5431")
DB_USER = os.getenv("DB_USER", "Rokeeb")
DB_NAME = os.getenv("DB_NAME", "stablecoin-db")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rokeeb123")


COINGECKO_BASE_URL =    "https://api.coingecko.com/api/v3"
COINGECKO_TIMEOUT =     30
COINGECKO_CATEGORY =    "stablecoins"
STABLECOIN_PEG_TARGET = 1.00


DEPEG_THRESHOLDS = {
    "low":      0.1,
    "medium":   0.5,
    "critical": 1.0
}

STRESS_WEIGHTS = {
    "depeg":       0.40,
    "liquidity":   0.34,
    "utilization": 0.25
}


FETCH_INTERVAL_MINUTES = 5
BATCH_SIZE =             250
RATE_LIMIT_PAUSE =       2


RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"
LOG_PATH = "logs/stablecoin_tracker.log"
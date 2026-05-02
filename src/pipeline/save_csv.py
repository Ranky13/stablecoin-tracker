import os
import logging
import pandas as pd
from datetime import datetime
from config.setting import PROCESSED_DATA_PATH

logger = logging.getLogger(__name__)


def save_csv(df):

    logger.info("🔄 Saving data to CSV...")

    try:
        
        os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filepath = f"{PROCESSED_DATA_PATH}stablecoins_{timestamp}.csv"

        df.to_csv(filepath, index=False)

        logger.info(f"✅ CSV saved to {filepath}")
        logger.info(f"📊 {len(df)} records saved")

        return filepath

    except Exception as e:
        logger.error(f"❌ Error saving CSV: {e}")
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from src.pipeline.extract import extract
    from src.pipeline.transform import transform
    from src.pipeline.validate import validate

    raw_data = extract()
    if raw_data:
        df       = transform(raw_data)
        valid_df = validate(df)
        filepath = save_csv(valid_df)
        if filepath:
            print(f"\n✅ CSV saved to {filepath}")
            print(f"\n📊 Preview:")
            print(pd.read_csv(filepath).head())
        else:
            print("\n❌ CSV saving failed")
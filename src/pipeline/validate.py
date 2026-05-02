import logging
import pandas as pd

logger = logging.getLogger(__name__)


def validate(df):
   
    logger.info("🔄 Starting validation...")
    logger.info(f"📊 Validating {len(df)} stablecoins")

    # Track how many rows we start with
    initial_count = len(df)


    invalid_symbols = df[
        df['symbol'].isna() | (df['symbol'] == '')
    ]
    if len(invalid_symbols) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_symbols)} coins "
            f"with missing symbols"
        )
    df = df[df['symbol'].notna() & (df['symbol'] != '')]

   
    invalid_prices = df[
        (df['price'] < 0.50) | (df['price'] > 1.50)
    ]
    if len(invalid_prices) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_prices)} coins "
            f"with invalid prices: "
            f"{invalid_prices['symbol'].tolist()}"
        )
    df = df[(df['price'] >= 0.50) & (df['price'] <= 1.50)]

   
    invalid_depeg_filter = df[df['depeg_score'] > 5.0]
    if len(invalid_depeg_filter) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_depeg_filter)} "
            f"non USD pegged coins: "
            f"{invalid_depeg_filter['symbol'].tolist()}"
        )
    df = df[df['depeg_score'] <= 5.0]

 
    invalid_market_cap = df[df['market_cap'] <= 0]
    if len(invalid_market_cap) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_market_cap)} coins "
            f"with invalid market cap"
        )
    df = df[df['market_cap'] > 0]

 
    invalid_supply = df[df['circulating_supply'] <= 0]
    if len(invalid_supply) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_supply)} coins "
            f"with invalid circulating supply"
        )
    df = df[df['circulating_supply'] > 0]

  
    invalid_depeg = df[
        (df['depeg_score'] < 0) | (df['depeg_score'] > 100)
    ]
    if len(invalid_depeg) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_depeg)} coins "
            f"with invalid depeg score"
        )
    df = df[
        (df['depeg_score'] >= 0) & (df['depeg_score'] <= 100)
    ]

  
    invalid_stress = df[
        (df['stress_index'] < 0) | (df['stress_index'] > 100)
    ]
    if len(invalid_stress) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_stress)} coins "
            f"with invalid stress index"
        )
    df = df[
        (df['stress_index'] >= 0) & (df['stress_index'] <= 100)
    ]

    
    invalid_util = df[
        (df['utilization'] < 0) | (df['utilization'] > 100)
    ]
    if len(invalid_util) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_util)} coins "
            f"with invalid utilization"
        )
    df = df[
        (df['utilization'] >= 0) & (df['utilization'] <= 100)
    ]

  
    invalid_liquidity = df[df['liquidity_ratio'] < 0]
    if len(invalid_liquidity) > 0:
        logger.warning(
            f"⚠️ Removing {len(invalid_liquidity)} coins "
            f"with invalid liquidity ratio"
        )
    df = df[df['liquidity_ratio'] >= 0]

    
    duplicates = df[df.duplicated(subset=['symbol'])]
    if len(duplicates) > 0:
        logger.warning(
            f"⚠️ Removing {len(duplicates)} "
            f"duplicate symbols: "
            f"{duplicates['symbol'].tolist()}"
        )
    df = df.drop_duplicates(subset=['symbol'])

 
    inactive_coins = df[df['velocity'] == 0]
    if len(inactive_coins) > 0:
        logger.warning(
            f"⚠️ Removing {len(inactive_coins)} "
            f"inactive coins with zero velocity: "
            f"{inactive_coins['symbol'].tolist()}"
        )
    df = df[df['velocity'] > 0]

 
    final_count   = len(df)
    removed_count = initial_count - final_count

    if removed_count > 0:
        logger.warning(
            f"⚠️ Removed {removed_count} invalid records "
            f"out of {initial_count}"
        )
    else:
        logger.info(
            f"✅ All {initial_count} records passed validation"
        )

    logger.info(
        f"✅ Validation complete. "
        f"{final_count} valid stablecoins ready for database"
    )

    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from src.pipeline.extract import extract
    from src.pipeline.transform import transform

    raw_data = extract()
    if raw_data:
        df = transform(raw_data)
        validated_df = validate(df)
        print(f"\n📊 Before validation: {len(df)} coins")
        print(f"📊 After validation:  {len(validated_df)} coins")
        print(f"\n📊 Sample validated data:")
        print(validated_df.head())
        print(f"\n📊 Max depeg score: {validated_df['depeg_score'].max()}")
        print(f"📊 Min depeg score: {validated_df['depeg_score'].min()}")
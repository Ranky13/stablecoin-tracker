import logging
import pandas as pd
from datetime import datetime
from src.metrics.depeg_score import calculate_depeg_score
from src.metrics.market_share import calculate_market_share
from src.metrics.velocity import calculate_velocity
from src.metrics.liquidity_ratio import calculate_liquidity_ratio
from src.metrics.utilization import calculate_utilization
from src.metrics.supply_change import calculate_supply_change
from src.metrics.stress_index import calculate_stress_index
from config.setting import STABLECOIN_PEG_TARGET

logger = logging.getLogger(__name__)


def transform(raw_data):
    """
    Cleans and transforms raw CoinGecko data.
    Calculates all 8 metrics for each stablecoin.
    Returns clean pandas DataFrame for validate.py
    """
    logger.info("🔄 Starting transformation...")

    
    df = pd.DataFrame(raw_data)
    logger.info(f"📊 Processing {len(df)} stablecoins")

 
    df = df[[
        'id',
        'symbol',
        'name',
        'current_price',
        'market_cap',
        'total_volume',
        'circulating_supply',
        'total_supply',
        'price_change_24h',
        'market_cap_change_24h'
    ]]


    df = df.rename(columns={
        'current_price':         'price',
        'total_volume':          'transaction_volume',
        'market_cap_change_24h': 'market_cap_change'
    })


    numeric_columns = [
        'price',
        'market_cap',
        'transaction_volume',
        'circulating_supply',
        'total_supply',
        'price_change_24h',
        'market_cap_change'
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    
    df = df.fillna(0)

  
    df = df.drop_duplicates(subset=['symbol'])
    

    df = df[df['price'] >= 0]

   
    df = df[df['circulating_supply'] >= 0]

    df['total_supply'] = df.apply(
        lambda row: row['circulating_supply']
        if row['total_supply'] < row['circulating_supply']
        else row['total_supply'], axis=1
    )


    df['peg_target'] = STABLECOIN_PEG_TARGET

    logger.info(f"✅ Cleaning complete. {len(df)} valid stablecoins")

 

    total_market_cap = df['market_cap'].sum()


    df['depeg_score']     = df['price'].apply(
        lambda x: calculate_depeg_score(x)
    )
    df['market_share']    = df['market_cap'].apply(
        lambda x: calculate_market_share(x, total_market_cap)
    )
    df['velocity']        = df.apply(
        lambda row: calculate_velocity(
            row['transaction_volume'],
            row['market_cap']
        ), axis=1
    )
    df['liquidity_ratio'] = df.apply(
        lambda row: calculate_liquidity_ratio(
            row['transaction_volume'],
            row['circulating_supply']
        ), axis=1
    )
    df['utilization']     = df.apply(
        lambda row: calculate_utilization(
            row['circulating_supply'],
            row['total_supply']
        ), axis=1
    )
    df['supply_change']   = df.apply(
        lambda row: calculate_supply_change(
            row['circulating_supply'],
            row['price_change_24h']
        ), axis=1
    )

    df['volume_to_market_cap'] = df.apply(
    lambda row: round(
        row['transaction_volume'] / row['market_cap'], 6
    ) if row['market_cap'] > 0 else 0,
    axis=1
)
    df['stress_index']    = df.apply(
        lambda row: calculate_stress_index(
            row['depeg_score'],
            row['liquidity_ratio'],
            row['utilization']
        ), axis=1
    )

    
    df['recorded_at'] = datetime.now()

    logger.info("✅ Transformation complete!")
    logger.info(f"📊 Columns: {list(df.columns)}")

    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from src.pipeline.extract import extract
    raw_data = extract()
    if raw_data:
        df = transform(raw_data)
        print("\n📊 Sample transformed data:")
        print(df.head())
        print(f"\n📊 Shape: {df.shape}")
        print(f"\n📊 Columns: {list(df.columns)}")
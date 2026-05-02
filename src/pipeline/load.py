import logging
import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import (
    Base,
    StablecoinPrice,
    SupplyMetric,
    ActivityMetric,
    LiquidityMetric,
    RiskMetric
)
from config.setting import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

load_dotenv()
logger = logging.getLogger(__name__)


def get_engine():
    
    connection_string = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(connection_string)


def get_session():
    
    engine  = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def get_psycopg2_connection():
 
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return None


def load(df):

    logger.info("🔄 Starting database load...")
    logger.info(f"📊 Loading {len(df)} stablecoins")

    session     = get_session()
    saved_count = 0

    try:
        for _, row in df.iterrows():

      
            existing_price = session.query(StablecoinPrice).filter(
                StablecoinPrice.symbol == row['symbol']
            ).first()

            if existing_price:
                existing_price.price       = float(row['price'])
                existing_price.market_cap  = float(row['market_cap'])
                existing_price.depeg_score = float(row['depeg_score'])
                existing_price.price_change_24hr = float(row['price_change_24h'])
                existing_price.updated_at  = row['recorded_at']
            else:
                session.add(StablecoinPrice(
                    symbol      = row['symbol'],
                    price       = float(row['price']),
                    market_cap  = float(row['market_cap']),
                    depeg_score = float(row['depeg_score']),
                    price_change_24h = float(row['price_change_24'])
                ))

  
            existing_supply = session.query(SupplyMetric).filter(
                SupplyMetric.symbol == row['symbol']
            ).first()

            if existing_supply:
                existing_supply.total_supply       = float(row['total_supply'])
                existing_supply.circulating_supply = float(row['circulating_supply'])
                existing_supply.supply_change      = float(row['supply_change'])
                existing_supply.market_share       = float(row['market_share'])
                existing_supply.updated_at         = row['recorded_at']
            else:
                session.add(SupplyMetric(
                    symbol             = row['symbol'],
                    total_supply       = float(row['total_supply']),
                    circulating_supply = float(row['circulating_supply']),
                    supply_change      = float(row['supply_change']),
                    market_share       = float(row['market_share'])
                ))

          
            existing_activity = session.query(ActivityMetric).filter(
                ActivityMetric.symbol == row['symbol']
            ).first()

            if existing_activity:
                existing_activity.transaction_volume = float(row['transaction_volume'])
                existing_activity.velocity           = float(row['velocity'])
                existing_activity.utilization        = float(row['utilization'])
                existing_activity.updated_at         = row['recorded_at']
            else:
                session.add(ActivityMetric(
                    symbol             = row['symbol'],
                    transaction_volume = float(row['transaction_volume']),
                    velocity           = float(row['velocity']),
                    utilization        = float(row['utilization']),
                    volume_to_market_cap = float(row['volume_to_market_cap'])
                ))

          
            existing_liquidity = session.query(LiquidityMetric).filter(
                LiquidityMetric.symbol == row['symbol']
            ).first()

            if existing_liquidity:
                existing_liquidity.pool_depth      = float(row['transaction_volume'])
                existing_liquidity.liquidity_ratio = float(row['liquidity_ratio'])
                existing_liquidity.updated_at      = row['recorded_at']
            else:
                session.add(LiquidityMetric(
                    symbol          = row['symbol'],
                    pool_depth      = float(row['transaction_volume']),
                    liquidity_ratio = float(row['liquidity_ratio'])
                ))

            
            existing_risk = session.query(RiskMetric).filter(
                RiskMetric.symbol == row['symbol']
            ).first()

            if existing_risk:
                existing_risk.stress_index = float(row['stress_index'])
                existing_risk.depeg_score  = float(row['depeg_score'])
                existing_risk.updated_at   = row['recorded_at']
            else:
                session.add(RiskMetric(
                    symbol       = row['symbol'],
                    stress_index = float(row['stress_index']),
                    depeg_score  = float(row['depeg_score'])
                ))

            saved_count += 1

        session.commit()
        logger.info(
            f"✅ Successfully upserted {saved_count} "
            f"stablecoins to all five tables"
        )
        return True

    except Exception as e:
        session.rollback()
        logger.error(f"❌ Database load failed: {e}")
        return False

    finally:
        session.close()
        logger.info("✅ Database session closed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from src.pipeline.extract import extract
    from src.pipeline.transform import transform
    from src.pipeline.validate import validate

    raw_data = extract()
    if raw_data:
        df       = transform(raw_data)
        valid_df = validate(df)
        success  = load(valid_df)
        if success:
            print("\n✅ Data successfully loaded to PostgreSQL!")
        else:
            print("\n❌ Loading failed. Check logs for details.")
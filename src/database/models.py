from sqlalchemy import (
    Column, Integer, String,
    Numeric, TIMESTAMP, text
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StablecoinPrice(Base):
   
    __tablename__ = "stablecoin_prices"

    id          = Column(Integer, primary_key=True)
    symbol      = Column(String(20), nullable=False)
    price       = Column(Numeric(18, 8), nullable=False)
    market_cap  = Column(Numeric(30, 2))
    depeg_score = Column(Numeric(10, 6))
    recorded_at = Column(TIMESTAMP, server_default=text("NOW()"))
    created_at  = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at  = Column(TIMESTAMP, server_default=text("NOW()"),
                         onupdate=text("NOW()"))

    def __repr__(self):
        return (
            f"<StablecoinPrice("
            f"symbol='{self.symbol}', "
            f"price={self.price}, "
            f"market_cap={self.market_cap}, "
            f"depeg_score={self.depeg_score}, "
            f"recorded_at={self.recorded_at}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )


class SupplyMetric(Base):

    __tablename__ = "supply_metrics"

    id                 = Column(Integer, primary_key=True)
    symbol             = Column(String(20), nullable=False)
    total_supply       = Column(Numeric(30, 2))
    circulating_supply = Column(Numeric(30, 2))
    supply_change      = Column(Numeric(20, 2))
    market_share       = Column(Numeric(10, 6))
    recorded_at        = Column(TIMESTAMP, server_default=text("NOW()"))
    created_at         = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at         = Column(TIMESTAMP, server_default=text("NOW()"),
                                onupdate=text("NOW()"))

    def __repr__(self):
        return (
            f"<SupplyMetric("
            f"symbol='{self.symbol}', "
            f"total_supply={self.total_supply}, "
            f"circulating_supply={self.circulating_supply}, "
            f"supply_change={self.supply_change}, "
            f"market_share={self.market_share}, "
            f"recorded_at={self.recorded_at}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )


class ActivityMetric(Base):
 
    __tablename__ = "activity_metrics"

    id                    = Column(Integer, primary_key=True)
    symbol                = Column(String(20), nullable=False)
    transaction_volume    = Column(Numeric(30, 2))
    velocity              = Column(Numeric(10, 6))
    utilization           = Column(Numeric(10, 6))
    volume_to_market_cap  = Column(Numeric(10, 6))
    recorded_at           = Column(TIMESTAMP, server_default=text("NOW()"))
    created_at            = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at            = Column(TIMESTAMP, server_default=text("NOW()"),
                                onupdate=text("NOW()"))

    def __repr__(self):
        return (
            f"<ActivityMetric("
            f"symbol='{self.symbol}', "
            f"transaction_volume={self.transaction_volume}, "
            f"velocity={self.velocity}, "
            f"utilization={self.utilization}, "
            f"recorded_at={self.recorded_at}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )


class LiquidityMetric(Base):
    
    __tablename__ = "liquidity_metrics"

    id              = Column(Integer, primary_key=True)
    symbol          = Column(String(20), nullable=False)
    pool_depth      = Column(Numeric(30, 2))
    liquidity_ratio = Column(Numeric(10, 6))
    recorded_at     = Column(TIMESTAMP, server_default=text("NOW()"))
    created_at      = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at      = Column(TIMESTAMP, server_default=text("NOW()"),
                             onupdate=text("NOW()"))

    def __repr__(self):
        return (
            f"<LiquidityMetric("
            f"symbol='{self.symbol}', "
            f"pool_depth={self.pool_depth}, "
            f"liquidity_ratio={self.liquidity_ratio}, "
            f"recorded_at={self.recorded_at}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )


class RiskMetric(Base):
 
    __tablename__ = "risk_metrics"

    id           = Column(Integer, primary_key=True)
    symbol       = Column(String(20), nullable=False)
    stress_index = Column(Numeric(10, 6))
    depeg_score  = Column(Numeric(10, 6))
    recorded_at  = Column(TIMESTAMP, server_default=text("NOW()"))
    created_at   = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at   = Column(TIMESTAMP, server_default=text("NOW()"),
                          onupdate=text("NOW()"))

    def __repr__(self):
        return (
            f"<RiskMetric("
            f"symbol='{self.symbol}', "
            f"stress_index={self.stress_index}, "
            f"depeg_score={self.depeg_score}, "
            f"recorded_at={self.recorded_at}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )
import logging

logger = logging.getLogger(__name__)


def calculate_velocity(transaction_volume, market_cap):
    
    try:
        if transaction_volume is None or transaction_volume < 0:
            logger.warning(
                f"Invalid transaction volume: {transaction_volume}"
            )
            return 0.0

        if market_cap is None or market_cap <= 0:
            logger.warning(
                f"Invalid market cap: {market_cap}"
            )
            return 0.0

        velocity = transaction_volume / market_cap

        velocity = round(velocity, 6)

        if velocity >= 2.0:
            logger.warning(
                f"Extremely high velocity: {velocity} "
                f"could indicate wash trading"
            )
        elif velocity >= 1.0:
            logger.info(
                f"High velocity detected: {velocity}"
            )
        elif velocity <= 0.01:
            logger.info(
                f"Very low velocity detected: {velocity} "
                f"coin may be illiquid"
            )

        return velocity

    except Exception as e:
        logger.error(f" Error calculating velocity: {e}")
        return 0.0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_coins = {
        "USDT":        (45_000_000_000, 95_000_000_000),
        "USDC":        (20_000_000_000, 45_000_000_000),
        "DAI":         (500_000_000,    5_000_000_000),
        "Small Coin":  (100_000,        10_000_000),
    }

    print("Velocity Tests:")
    print("─" * 60)
    for symbol, (volume, market_cap) in test_coins.items():
        velocity = calculate_velocity(volume, market_cap)
        print(
            f"{symbol:12} | "
            f"Volume: ${volume:,} | "
            f"Velocity: {velocity}"
        )
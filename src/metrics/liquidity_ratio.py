import logging

logger = logging.getLogger(__name__)


def calculate_liquidity_ratio(transaction_volume, circulating_supply):
   
    try:
        if transaction_volume is None or transaction_volume < 0:
            logger.warning(
                f"Invalid transaction volume: {transaction_volume}"
            )
            return 0.0

        if circulating_supply is None or circulating_supply <= 0:
            logger.warning(
                f"Invalid circulating supply: {circulating_supply}"
            )
            return 0.0

        liquidity_ratio = transaction_volume / circulating_supply

        liquidity_ratio = round(liquidity_ratio, 6)

        if liquidity_ratio <= 0.01:
            logger.warning(
                f"Very low liquidity ratio: {liquidity_ratio} "
                f"coin may be difficult to trade"
            )
        elif liquidity_ratio <= 0.05:
            logger.info(
                f"Low liquidity ratio: {liquidity_ratio}"
            )
        elif liquidity_ratio >= 1.0:
            logger.info(
                f"High liquidity ratio: {liquidity_ratio}"
            )

        return liquidity_ratio

    except Exception as e:
        logger.error(f"Error calculating liquidity ratio: {e}")
        return 0.0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test with different scenarios
    test_coins = {
        "USDT":          (45_000_000_000, 95_000_000_000),
        "USDC":          (20_000_000_000, 45_000_000_000),
        "DAI":           (500_000_000,    5_000_000_000),
        "Illiquid Coin": (10_000,         10_000_000),
    }

    print("Liquidity Ratio Tests:")
    print("─" * 65)
    for symbol, (volume, supply) in test_coins.items():
        ratio = calculate_liquidity_ratio(volume, supply)
        print(
            f"{symbol:15} | "
            f"Volume: ${volume:,} | "
            f"Supply: {supply:,} | "
            f"Ratio: {ratio}"
        )
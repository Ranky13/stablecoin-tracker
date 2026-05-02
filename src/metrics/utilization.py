import logging

logger = logging.getLogger(__name__)


def calculate_utilization(circulating_supply, total_supply):

    try:
        if circulating_supply is None or circulating_supply < 0:
            logger.warning(
                f"Invalid circulating supply: {circulating_supply}"
            )
            return 0.0

        if total_supply is None or total_supply <= 0:
            logger.warning(
                f"Invalid total supply: {total_supply}"
            )
            return 0.0

    
        if circulating_supply > total_supply:
            logger.warning(
                f"Circulating supply {circulating_supply} "
                f"exceeds total supply {total_supply} "
                f"using circulating supply as total"
            )
            total_supply = circulating_supply

        utilization = (circulating_supply / total_supply) * 100

        utilization = round(utilization, 6)

        if utilization >= 99.0:
            logger.warning(
                f"Near maximum utilization: {utilization}% "
                f"very little supply buffer remaining"
            )
        elif utilization >= 90.0:
            logger.info(
                f"High utilization: {utilization}%"
            )
        elif utilization <= 20.0:
            logger.warning(
                f"Very low utilization: {utilization}% "
                f"large portion of supply is locked"
            )

        return utilization

    except Exception as e:
        logger.error(f"Error calculating utilization: {e}")
        return 0.0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_coins = {
        "USDT":         (95_000_000_000,  100_000_000_000),
        "USDC":         (45_000_000_000,  50_000_000_000),
        "DAI":          (5_000_000_000,   5_000_000_000),
        "Low Util":     (1_000_000_000,   100_000_000_000),
    }

    print("Utilization Tests:")
    print("─" * 70)
    for symbol, (circulating, total) in test_coins.items():
        util = calculate_utilization(circulating, total)
        print(
            f"{symbol:12} | "
            f"Circulating: {circulating:,} | "
            f"Total: {total:,} | "
            f"Utilization: {util}%"
        )
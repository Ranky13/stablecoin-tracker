import logging

logger = logging.getLogger(__name__)


def calculate_supply_change(circulating_supply, price_change_24h):
   
    try:
        if circulating_supply is None or circulating_supply < 0:
            logger.warning(
                f"⚠️ Invalid circulating supply: {circulating_supply}"
            )
            return 0.0

        if price_change_24h is None:
            logger.warning(
                f"Invalid price change: {price_change_24h}"
            )
            return 0.0

        supply_change = circulating_supply * price_change_24h

        supply_change = round(supply_change, 2)

        if supply_change > 0:
            logger.info(
                f"Minting detected: "
                f"+{supply_change:,.2f} coins added to supply"
            )
        elif supply_change < 0:
            logger.info(
                f"Burning detected: "
                f"{supply_change:,.2f} coins removed from supply"
            )
        else:
            logger.info(
                f"Supply stable: no significant change"
            )

        supply_change_pct = abs(price_change_24h) * 100
        if supply_change_pct >= 5.0:
            logger.warning(
                f"Large supply change detected: "
                f"{supply_change_pct:.2f}% change in 24h "
                f"this could impact the peg"
            )
        elif supply_change_pct >= 2.0:
            logger.warning(
                f"⚠️ Moderate supply change: "
                f"{supply_change_pct:.2f}% change in 24h"
            )

        return supply_change

    except Exception as e:
        logger.error(f"Error calculating supply change: {e}")
        return 0.0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_coins = {
        "USDT Minting":  (95_000_000_000, 0.001),
        "USDC Burning":  (45_000_000_000, -0.002),
        "DAI Stable":    (5_000_000_000,  0.0),
        "Large Change":  (10_000_000_000, 0.06),
    }

    print("Supply Change Tests:")
    print("─" * 70)
    for scenario, (supply, price_change) in test_coins.items():
        change = calculate_supply_change(supply, price_change)
        print(
            f"{scenario:15} | "
            f"Supply: {supply:,} | "
            f"Price Change: {price_change} | "
            f"Supply Change: {change:,.2f}"
        )
import logging
from config.setting import STABLECOIN_PEG_TARGET, DEPEG_THRESHOLDS

logger = logging.getLogger(__name__)


def calculate_depeg_score(price):
    """
    Calculates how far a stablecoin has deviated from its peg.
    
    Parameters:
        price → current price of the stablecoin from CoinGecko
    
    Returns:
        depeg_score → percentage deviation from $1.00 peg
    
    Example:
        price = 0.95
        depeg_score = 5.0%
    """
    try:
        # Step 1: Handle invalid price values
        if price is None or price <= 0:
            logger.warning(f"⚠️ Invalid price value: {price}")
            return 0.0

        # Step 2: Calculate deviation from peg
        depeg_score = abs(price - STABLECOIN_PEG_TARGET) / STABLECOIN_PEG_TARGET * 100

        # Step 3: Round to 6 decimal places
        depeg_score = round(depeg_score, 6)

        # Step 4: Determine severity
        if depeg_score >= DEPEG_THRESHOLDS["critical"]:
            logger.warning(
                f"🚨 CRITICAL depeg detected: {depeg_score}%"
            )
        elif depeg_score >= DEPEG_THRESHOLDS["medium"]:
            logger.warning(
                f"⚠️ MEDIUM depeg detected: {depeg_score}%"
            )
        elif depeg_score >= DEPEG_THRESHOLDS["low"]:
            logger.info(
                f"📊 LOW depeg detected: {depeg_score}%"
            )

        return depeg_score

    except Exception as e:
        logger.error(f"❌ Error calculating depeg score: {e}")
        return 0.0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test with different prices
    test_prices = {
        "Normal":   1.0001,
        "Low":      0.999,
        "Medium":   0.995,
        "Critical": 0.98
    }

    print("📊 Depeg Score Tests:")
    print("─" * 40)
    for scenario, price in test_prices.items():
        score = calculate_depeg_score(price)
        print(f"{scenario:10} | Price: ${price} | Depeg: {score}%")
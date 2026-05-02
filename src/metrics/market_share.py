import logging
from config.setting import DEPEG_THRESHOLDS

logger = logging.getLogger(__name__)


def calculate_market_share(market_cap, total_market_cap):
    """
    Calculates the market share of a stablecoin
    relative to the total stablecoin market.
    
    Parameters:
        market_cap       → market cap of one stablecoin
        total_market_cap → combined market cap of all stablecoins
    
    Returns:
        market_share → percentage of total market this coin holds
    
    Example:
        USDT market cap = $95 billion
        Total market cap = $180 billion
        market_share = 52.7%
    """
    try:
        # Step 1: Handle invalid values
        if market_cap is None or market_cap <= 0:
            logger.warning(f"⚠️ Invalid market cap: {market_cap}")
            return 0.0

        if total_market_cap is None or total_market_cap <= 0:
            logger.warning(
                f"⚠️ Invalid total market cap: {total_market_cap}"
            )
            return 0.0

        # Step 2: Calculate market share
        market_share = (market_cap / total_market_cap) * 100

        # Step 3: Round to 6 decimal places
        market_share = round(market_share, 6)

        # Step 4: Log dominant coins
        if market_share >= 50:
            logger.warning(
                f"🚨 Dominant coin detected: {market_share}% market share"
            )
        elif market_share >= 25:
            logger.info(
                f"📊 Large market share detected: {market_share}%"
            )

        return market_share

    except Exception as e:
        logger.error(f"❌ Error calculating market share: {e}")
        return 0.0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test with different market caps
    test_coins = {
        "USDT": 95_000_000_000,
        "USDC": 45_000_000_000,
        "DAI":  5_000_000_000,
        "FRAX": 1_000_000_000
    }

    total = sum(test_coins.values())

    print("📊 Market Share Tests:")
    print("─" * 50)
    for symbol, market_cap in test_coins.items():
        share = calculate_market_share(market_cap, total)
        print(f"{symbol:6} | Market Cap: ${market_cap:,} | Share: {share}%")
import logging
from config.setting import STRESS_WEIGHTS, DEPEG_THRESHOLDS

logger = logging.getLogger(__name__)


def calculate_stress_index(depeg_score, liquidity_ratio, utilization):

    try:
        if depeg_score is None or depeg_score < 0:
            logger.warning(
                f"Invalid depeg score: {depeg_score}"
            )
            depeg_score = 0.0

        if liquidity_ratio is None or liquidity_ratio < 0:
            logger.warning(
                f"Invalid liquidity ratio: {liquidity_ratio}"
            )
            liquidity_ratio = 0.0

        if utilization is None or utilization < 0:
            logger.warning(
                f"Invalid utilization: {utilization}"
            )
            utilization = 0.0

        depeg_component = min(depeg_score * 10, 100)

    
        liquidity_component = max(0, 100 - (liquidity_ratio * 100))

      
        utilization_component = abs(utilization - 80) / 80 * 100

        stress_index = (
            (depeg_component     * STRESS_WEIGHTS["depeg"]) +
            (liquidity_component * STRESS_WEIGHTS["liquidity"]) +
            (utilization_component * STRESS_WEIGHTS["utilization"])
        )

        stress_index = max(0, min(100, stress_index))

        stress_index = round(stress_index, 6)

        if stress_index >= 75:
            logger.warning(
                f"CRITICAL stress level: {stress_index} "
                f"immediate attention required"
            )
        elif stress_index >= 50:
            logger.warning(
                f"HIGH stress level: {stress_index} "
                f"monitor closely"
            )
        elif stress_index >= 25:
            logger.info(
                f"MEDIUM stress level: {stress_index}"
            )
        else:
            logger.info(
                f"LOW stress level: {stress_index}"
            )

        return stress_index

    except Exception as e:
        logger.error(f"Error calculating stress index: {e}")
        return 0.0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_coins = {
        "Healthy Coin": (0.01,  0.5,  90.0),
        "Medium Risk":  (0.5,   0.1,  70.0),
        "High Risk":    (1.0,   0.05, 50.0),
        "Critical":     (2.0,   0.01, 20.0),
    }

    print("Stress Index Tests:")
    print("─" * 75)
    for scenario, (depeg, liquidity, util) in test_coins.items():
        stress = calculate_stress_index(depeg, liquidity, util)
        print(
            f"{scenario:15} | "
            f"Depeg: {depeg}% | "
            f"Liquidity: {liquidity} | "
            f"Util: {util}% | "
            f"Stress: {stress}"
        )
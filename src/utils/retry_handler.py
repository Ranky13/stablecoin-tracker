import time
import logging

logger = logging.getLogger(__name__)

def retry (func, retries=3, delay=5):
    for attempt in range(retries):
        try:
            result = func()
            return result
        except Exception as e:
            logger.warning(
                f"Attempt {attempt + 1} of {retries} failed: (e)"
            )
            if attempt < retries -1:
                logger.warning(f"Retrying in {delay} seconds..")
                time.sleep(delay)
            else:
                logger.error(f"All {retries} attempt failed")
                return None
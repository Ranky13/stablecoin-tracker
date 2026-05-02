import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from config.setting import LOG_PATH


def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
   
    logger = logging.getLogger(name)
    logger.setLevel(level)

  
    if logger.handlers:
        return logger


    log_dir = os.path.dirname(LOG_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

   
    log_format = logging.Formatter(
        fmt=(
            '%(asctime)s | '
            '%(levelname)-8s | '
            '%(name)s | '
            '%(message)s'
        ),
        datefmt='%Y-%m-%d %H:%M:%S'
    )

   
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(log_format)


    file_handler = RotatingFileHandler(
        filename=LOG_PATH,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(log_format)


    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_pipeline_logger():

    return setup_logger('stablecoin.pipeline')


def get_api_logger():
    """
    Returns a logger specifically for
    the CoinGecko API client
    """
    return setup_logger('stablecoin.api')


def get_dashboard_logger():
    """
    Returns a logger specifically for
    the Streamlit dashboard
    """
    return setup_logger('stablecoin.dashboard')


def log_pipeline_start():
    """
    Logs a formatted pipeline start message
    """
    logger = get_pipeline_logger()
    logger.info("=" * 60)
    logger.info(
        f"🚀 Pipeline started at "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    logger.info("=" * 60)


def log_pipeline_end(success: bool, records: int = 0):
    """
    Logs a formatted pipeline end message

    Parameters:
        success → True if pipeline completed successfully
        records → number of records processed
    """
    logger = get_pipeline_logger()
    logger.info("=" * 60)

    if success:
        logger.info(
            f"✅ Pipeline completed successfully at "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        logger.info(f"📊 Records processed: {records}")
    else:
        logger.error(
            f"❌ Pipeline failed at "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    logger.info("=" * 60)


if __name__ == "__main__":
    # Test the logger
    logger = setup_logger(__name__)

    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")

    log_pipeline_start()
    log_pipeline_end(success=True, records=180)

    print(f"\n✅ Logger test complete!")
    print(f"📄 Check logs/app.log for output")
import logging
import schedule
import time
from main import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def start_pipeline():
   
    logger.info("🚀 Starting Stablecoin Intelligence Dashboard")

    # Run pipeline immediately on startup
    logger.info("🔄 Running initial pipeline...")
    run_pipeline()

    # Schedule pipeline to run every 5 minutes
    schedule.every(5).minutes.do(run_pipeline)
    logger.info("⏰ Pipeline scheduled every 5 minutes")


def start_dashboard():
   
    import subprocess
    import sys
    logger.info("🌐 Starting dashboard...")
    subprocess.Popen([
        sys.executable, "-m",
        "streamlit", "run",
        "app/dashboard.py"
    ])
    logger.info("✅ Dashboard running at http://localhost:8501")


if __name__ == "__main__":
    start_pipeline()

    start_dashboard()

    
    logger.info("✅ Everything is running!")
    logger.info("📊 Dashboard: http://localhost:8501")
    logger.info("⏰ Pipeline: every 5 minutes")
    logger.info("Press Ctrl+C to stop")

    while True:
        schedule.run_pending()
        time.sleep(1)
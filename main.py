import logging
from src.utils.logger import setup_logger, log_pipeline_start, log_pipeline_end
from src.pipeline.extract import extract
from src.pipeline.transform import transform
from src.pipeline.validate import validate
from src.pipeline.load import load
from src.pipeline.save_csv import save_csv

logger = setup_logger(__name__)


def run_pipeline():
    
    log_pipeline_start()

    # Step 1: Extract
    raw_data = extract()
    if not raw_data:
        log_pipeline_end(success=False)
        return False

    # Step 2: Transform
    df = transform(raw_data)
    if df is None or len(df) == 0:
        log_pipeline_end(success=False)
        return False

    # Step 3: Validate
    valid_df = validate(df)
    if valid_df is None or len(valid_df) == 0:
        log_pipeline_end(success=False)
        return False

    # Step 4: Load to database
    success = load(valid_df)
    if not success:
        log_pipeline_end(success=False)
        return False

    # Step 5: Save CSV backup
    filepath = save_csv(valid_df)
    if not filepath:
        log_pipeline_end(success=False)
        return False

    log_pipeline_end(success=True, records=len(valid_df))
    return True


if __name__ == "__main__":
    run_pipeline()
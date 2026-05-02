from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)


default_args = {
    'owner':             'stablecoin_tracker',
    'depends_on_past':   False,
    'start_date':        days_ago(1),
    'email_on_failure':  False,
    'email_on_retry':    False,
    'retries':           3,
    'retry_delay':       timedelta(minutes=2),
    'execution_timeout': timedelta(minutes=10),
}


def run_extract(**context):
    """
    Task 1: Extract raw data from CoinGecko API
    Saves raw JSON to data/raw/ folder
    Returns data via XCom for next task
    """
    from src.pipeline.extract import extract

    logger.info("🔄 Airflow: Starting extraction task")
    data = extract()

    if not data:
        raise ValueError("❌ Extraction failed. No data returned.")

    logger.info(f"✅ Airflow: Extracted {len(data)} stablecoins")

    # Push data to XCom so transform task can use it
    context['ti'].xcom_push(key='raw_data', value=data)
    return len(data)


def run_transform(**context):
 
    from src.pipeline.transform import transform

    logger.info("🔄 Airflow: Starting transform task")

    # Pull raw data from previous task
    raw_data = context['ti'].xcom_pull(
        task_ids='extract_task',
        key='raw_data'
    )

    if not raw_data:
        raise ValueError("❌ No raw data received from extract task")

    df = transform(raw_data)

    if df is None or len(df) == 0:
        raise ValueError("❌ Transform returned empty DataFrame")

    logger.info(f"✅ Airflow: Transformed {len(df)} stablecoins")

    # Convert to dict for XCom storage
    context['ti'].xcom_push(
        key='transformed_data',
        value=df.to_dict('records')
    )
    return len(df)


def run_validate(**context):
    
    import pandas as pd
    from src.pipeline.validate import validate

    logger.info("🔄 Airflow: Starting validation task")

    # Pull transformed data from previous task
    transformed_data = context['ti'].xcom_pull(
        task_ids='transform_task',
        key='transformed_data'
    )

    if not transformed_data:
        raise ValueError("❌ No transformed data received")

    df = pd.DataFrame(transformed_data)
    validated_df = validate(df)

    if validated_df is None or len(validated_df) == 0:
        raise ValueError("❌ Validation returned empty DataFrame")

    logger.info(
        f"✅ Airflow: Validated {len(validated_df)} stablecoins"
    )

    context['ti'].xcom_push(
        key='validated_data',
        value=validated_df.to_dict('records')
    )
    return len(validated_df)


def run_load(**context):
   
    import pandas as pd
    from src.pipeline.load import load

    logger.info("🔄 Airflow: Starting load task")

    validated_data = context['ti'].xcom_pull(
        task_ids='validate_task',
        key='validated_data'
    )

    if not validated_data:
        raise ValueError("❌ No validated data received")

    df = pd.DataFrame(validated_data)
    success = load(df)

    if not success:
        raise ValueError("❌ Database load failed")

    logger.info(
        f"✅ Airflow: Loaded {len(df)} stablecoins to database"
    )
    return len(df)


def run_save_csv(**context):
    
    import pandas as pd
    from src.pipeline.save_csv import save_csv

    logger.info("🔄 Airflow: Starting CSV save task")

    validated_data = context['ti'].xcom_pull(
        task_ids='validate_task',
        key='validated_data'
    )

    if not validated_data:
        raise ValueError("❌ No validated data received")

    df = pd.DataFrame(validated_data)
    filepath = save_csv(df)

    if not filepath:
        raise ValueError("❌ CSV save failed")

    logger.info(f"✅ Airflow: CSV saved to {filepath}")
    return filepath


def check_depeg_alerts(**context):
   
    import pandas as pd
    from config.setting import DEPEG_THRESHOLDS

    logger.info("🔄 Airflow: Checking depeg alerts")

    validated_data = context['ti'].xcom_pull(
        task_ids='validate_task',
        key='validated_data'
    )

    if not validated_data:
        logger.warning("⚠️ No data for depeg check")
        return

    df = pd.DataFrame(validated_data)

    # Check for critical depegs
    critical = df[
        df['depeg_score'] >= DEPEG_THRESHOLDS['critical']
    ]
    medium = df[
        df['depeg_score'] >= DEPEG_THRESHOLDS['medium']
    ]

    if len(critical) > 0:
        logger.warning(
            f"🚨 CRITICAL DEPEG ALERT: "
            f"{critical['symbol'].tolist()} "
            f"are critically depegged"
        )

    if len(medium) > 0:
        logger.warning(
            f"⚠️ MEDIUM DEPEG ALERT: "
            f"{medium['symbol'].tolist()} "
            f"have medium depeg"
        )

    logger.info(
        f"✅ Airflow: Depeg check complete. "
        f"{len(critical)} critical, "
        f"{len(medium)} medium alerts"
    )
    return {
        'critical': critical['symbol'].tolist(),
        'medium':   medium['symbol'].tolist()
    }

with DAG(
    dag_id='stablecoin_pipeline',
    default_args=default_args,
    description=(
        'Fetches stablecoin data from CoinGecko '
        'calculates metrics and loads to PostgreSQL'
    ),
    schedule_interval='*/5 * * * *',  # every 5 minutes
    catchup=False,
    max_active_runs=1,
    tags=['stablecoin', 'crypto', 'pipeline']
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=run_extract,
        provide_context=True,
        doc_md="""
        ## Extract Task
        Fetches all 250+ stablecoins from CoinGecko API.
        Saves raw JSON backup to data/raw/ folder.
        """
    )

   
    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=run_transform,
        provide_context=True,
        doc_md="""
        ## Transform Task
        Cleans raw data and calculates all metrics:
        depeg score, market share, velocity,
        liquidity ratio, utilization, supply change,
        stress index
        """
    )

   
    validate_task = PythonOperator(
        task_id='validate_task',
        python_callable=run_validate,
        provide_context=True,
        doc_md="""
        
        
        """
    )

    
    load_task = PythonOperator(
        task_id='load_task',
        python_callable=run_load,
        provide_context=True,
        doc_md="""
      
        """
    )

    save_csv_task = PythonOperator(
        task_id='save_csv_task',
        python_callable=run_save_csv,
        provide_context=True,
        doc_md="""
       
        """
    )

   
    alert_task = PythonOperator(
        task_id='alert_task',
        python_callable=check_depeg_alerts,
        provide_context=True,
        doc_md="""
        
        """
    )

    extract_task >> transform_task >> validate_task >> load_task
    validate_task >> save_csv_task
    validate_task >> alert_task
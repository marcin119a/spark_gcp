import os

import pandas as pd  # type: ignore[import-untyped]
from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame

from us_accidents_etl.config.settings import ETLConfig, MLConfig

GCS_TEMP_BASE = "gs://plated-observer-474112-k0-airflow-spark-course-dags/temp_csv"


def _gcs_csv_to_local_parquet(gcs_csv_path: str, local_path: str) -> None:
    """Read CSV parts written by Spark from GCS, save as single local parquet."""
    os.makedirs(local_path, exist_ok=True)
    df = pd.read_csv(
        f"{gcs_csv_path}/*.csv",
        storage_options={"token": "google_default"},
        low_memory=False,
    )
    df.to_parquet(os.path.join(local_path, "data.parquet"), index=False)


def write_dataset(df: DataFrame, local_path: str, gcs_temp_path: str) -> None:
    if local_path.startswith("gs://") or local_path.startswith("s3://"):
        df.write.mode("overwrite").parquet(local_path)
    else:
        # Server writes CSV parts to GCS, client downloads via gcsfs + pandas
        df.write.mode("overwrite").option("header", "true").csv(gcs_temp_path)
        _gcs_csv_to_local_parquet(gcs_temp_path, local_path)


def write_model(model: PipelineModel, cfg: MLConfig) -> None:
    if cfg.model_path:
        model.write().overwrite().save(cfg.model_path)


def write_filtered(df: DataFrame, cfg: ETLConfig) -> None:
    write_dataset(df, f"{cfg.output_path}/filtered", f"{GCS_TEMP_BASE}/filtered")


def write_aggregations(
    severity: DataFrame,
    states: DataFrame,
    cities: DataFrame,
    weather: DataFrame,
    day_night: DataFrame,
    cfg: ETLConfig,
) -> None:
    agg_base = f"{cfg.output_path}/agg"
    gcs_base = f"{GCS_TEMP_BASE}/agg"
    write_dataset(severity, f"{agg_base}/severity_stats", f"{gcs_base}/severity_stats")
    write_dataset(states, f"{agg_base}/state_stats", f"{gcs_base}/state_stats")
    write_dataset(cities, f"{agg_base}/city_stats", f"{gcs_base}/city_stats")
    write_dataset(weather, f"{agg_base}/weather_stats", f"{gcs_base}/weather_stats")
    write_dataset(
        day_night, f"{agg_base}/day_night_stats", f"{gcs_base}/day_night_stats"
    )

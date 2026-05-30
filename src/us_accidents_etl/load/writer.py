import os

from pyspark.sql import DataFrame

from us_accidents_etl.config.settings import ETLConfig


def write_dataset(df: DataFrame, output_path: str) -> None:
    if output_path.startswith("gs://") or output_path.startswith("s3://"):
        df.write.mode("overwrite").parquet(output_path)
    else:
        os.makedirs(output_path, exist_ok=True)
        df.toPandas().to_parquet(os.path.join(output_path, "data.parquet"), index=False)


def write_filtered(df: DataFrame, cfg: ETLConfig) -> None:
    write_dataset(df, f"{cfg.output_path}/filtered")


def write_aggregations(
    severity: DataFrame,
    states: DataFrame,
    cities: DataFrame,
    weather: DataFrame,
    day_night: DataFrame,
    cfg: ETLConfig,
) -> None:
    agg_base = f"{cfg.output_path}/agg"
    write_dataset(severity,  f"{agg_base}/severity_stats")
    write_dataset(states,    f"{agg_base}/state_stats")
    write_dataset(cities,    f"{agg_base}/city_stats")
    write_dataset(weather,   f"{agg_base}/weather_stats")
    write_dataset(day_night, f"{agg_base}/day_night_stats")

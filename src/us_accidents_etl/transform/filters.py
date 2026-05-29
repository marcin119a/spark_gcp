from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from us_accidents_etl.config.settings import ETLConfig


def filter_high_severity(df: DataFrame, cfg: ETLConfig) -> DataFrame:
    return df.filter(F.col("Severity") >= cfg.min_severity)


def filter_weather_conditions(df: DataFrame, cfg: ETLConfig) -> DataFrame:
    return df.filter(F.col("Weather_Condition").isin(cfg.weather_conditions))


def apply_etl_filters(df: DataFrame, cfg: ETLConfig) -> DataFrame:
    return filter_weather_conditions(filter_high_severity(df, cfg), cfg)

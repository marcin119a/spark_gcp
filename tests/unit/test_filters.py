import pytest
from pyspark.sql import SparkSession

from us_accidents_etl.config.settings import ETLConfig
from us_accidents_etl.transform.filters import (
    apply_etl_filters,
    filter_high_severity,
    filter_weather_conditions,
)


@pytest.fixture
def etl_cfg() -> ETLConfig:
    return ETLConfig(
        input_path="gs://dummy/input",
        output_path="gs://dummy/output",
        min_severity=3,
        weather_conditions=["Rain", "Snow"],
    )


def test_filter_high_severity_keeps_only_matching_rows(
    spark: SparkSession, etl_cfg: ETLConfig
):
    df = spark.createDataFrame([(1,), (2,), (3,), (4,)], ["Severity"])
    result = filter_high_severity(df, etl_cfg)
    assert result.count() == 2
    assert result.filter("Severity < 3").count() == 0


def test_filter_weather_conditions_keeps_only_listed(
    spark: SparkSession, etl_cfg: ETLConfig
):
    df = spark.createDataFrame(
        [("Rain",), ("Snow",), ("Clear",), ("Fog",)], ["Weather_Condition"]
    )
    result = filter_weather_conditions(df, etl_cfg)
    assert result.count() == 2
    conditions = {row.Weather_Condition for row in result.collect()}
    assert conditions == {"Rain", "Snow"}


def test_apply_etl_filters_combines_both(spark: SparkSession, etl_cfg: ETLConfig):
    data = [
        (2, "Rain"),   # filtered: severity too low
        (3, "Clear"),  # filtered: wrong weather
        (3, "Rain"),   # kept
        (4, "Snow"),   # kept
    ]
    df = spark.createDataFrame(data, ["Severity", "Weather_Condition"])
    result = apply_etl_filters(df, etl_cfg)
    assert result.count() == 2

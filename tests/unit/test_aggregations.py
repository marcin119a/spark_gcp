from pyspark.sql import SparkSession

from us_accidents_etl.transform.aggregations import (
    city_stats,
    day_night_stats,
    severity_stats,
    state_stats,
    weather_stats,
)


def test_severity_stats_orders_by_count_desc(spark: SparkSession):
    data = [(2,), (2,), (3,), (4,), (2,)]
    df = spark.createDataFrame(data, ["Severity"])
    result = severity_stats(df)
    top = result.first()
    assert top.Severity == 2
    assert top.Total_Accidents == 3


def test_city_stats_respects_limit(spark: SparkSession):
    data = [("Miami",)] * 5 + [("Houston",)] * 3 + [("LA",)] * 7
    df = spark.createDataFrame(data, ["City"])
    result = city_stats(df, top_n=2)
    assert result.count() == 2
    assert result.first().City == "LA"


def test_state_stats_filters_below_threshold(spark: SparkSession):
    data = [("CA",)] * 20_000 + [("WY",)] * 500
    df = spark.createDataFrame(data, ["State"])
    result = state_stats(df, min_accidents=10_000)
    assert result.count() == 1
    assert result.first().State == "CA"


def test_weather_stats_counts_all_conditions(spark: SparkSession):
    data = [("Rain",), ("Rain",), ("Clear",)]
    df = spark.createDataFrame(data, ["Weather_Condition"])
    result = weather_stats(df)
    assert result.count() == 2
    assert result.first().Weather_Condition == "Rain"


def test_day_night_stats(spark: SparkSession):
    data = [("Day",), ("Day",), ("Night",)]
    df = spark.createDataFrame(data, ["Sunrise_Sunset"])
    result = day_night_stats(df)
    assert result.first().Sunrise_Sunset == "Day"
    assert result.first().Total_Accidents == 2

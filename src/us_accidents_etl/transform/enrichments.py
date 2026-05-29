from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def add_duration_minutes(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "Duration_Minutes",
        (F.unix_timestamp("End_Time") - F.unix_timestamp("Start_Time")) / 60,
    )


def add_time_features(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("Accident_Hour", F.hour("Start_Time"))
        .withColumn("Accident_DayOfWeek", F.dayofweek("Start_Time"))
        .withColumn("Accident_Month", F.month("Start_Time"))
        .withColumn("Accident_Year", F.year("Start_Time"))
    )


def enrich(df: DataFrame) -> DataFrame:
    return add_time_features(add_duration_minutes(df))

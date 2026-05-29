from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def severity_stats(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("Severity")
        .agg(F.count("*").alias("Total_Accidents"))
        .orderBy(F.desc("Total_Accidents"))
    )


def state_stats(df: DataFrame, min_accidents: int = 10_000) -> DataFrame:
    return (
        df.groupBy("State")
        .agg(F.count("*").alias("Total_Accidents"))
        .filter(F.col("Total_Accidents") > min_accidents)
        .orderBy(F.desc("Total_Accidents"))
    )


def city_stats(df: DataFrame, top_n: int = 10) -> DataFrame:
    return (
        df.groupBy("City")
        .agg(F.count("*").alias("Total_Accidents"))
        .orderBy(F.desc("Total_Accidents"))
        .limit(top_n)
    )


def weather_stats(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("Weather_Condition")
        .agg(F.count("*").alias("Total_Accidents"))
        .orderBy(F.desc("Total_Accidents"))
    )


def day_night_stats(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("Sunrise_Sunset")
        .agg(F.count("*").alias("Total_Accidents"))
        .orderBy(F.desc("Total_Accidents"))
    )

from pyspark.sql import DataFrame, SparkSession

from us_accidents_etl.config.settings import ETLConfig


def read_accidents_csv(spark: SparkSession, cfg: ETLConfig) -> DataFrame:
    return (
        spark.read.format("csv")
        .option("sep", ",")
        .option("inferSchema", "true")
        .option("header", "true")
        .load(cfg.input_path)
    )

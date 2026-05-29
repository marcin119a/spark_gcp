from pyspark.sql import SparkSession

from us_accidents_etl.config.settings import SparkConfig


def create_spark_session(spark_cfg: SparkConfig) -> SparkSession:
    if spark_cfg.remote:
        # spark.authenticate.secret is server-side only; clients must not set it
        return SparkSession.builder.remote(spark_cfg.remote).getOrCreate()

    return (
        SparkSession.builder.master(spark_cfg.master)
        .appName(spark_cfg.app_name)
        .config("spark.executor.memory", spark_cfg.executor_memory)
        .config("spark.driver.memory", spark_cfg.driver_memory)
        .config("spark.executor.cores", str(spark_cfg.executor_cores))
        .getOrCreate()
    )

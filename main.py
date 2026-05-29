import logging

from us_accidents_etl.config.settings import get_settings
from us_accidents_etl.pipeline import run
from us_accidents_etl.spark.session import create_spark_session

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)

if __name__ == "__main__":
    settings = get_settings()
    spark = create_spark_session(settings.spark)
    try:
        run(spark, settings)
    finally:
        spark.stop()

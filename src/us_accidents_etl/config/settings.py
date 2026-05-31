from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SparkConfig(BaseModel):
    master: str = "local[*]"
    remote: str | None = None  # sc://host:port — enables Spark Connect
    authenticate_secret: str | None = None
    app_name: str = "us-accidents-etl"
    executor_memory: str = "4g"
    driver_memory: str = "2g"
    executor_cores: int = 2


class ETLConfig(BaseModel):
    input_path: str  # gs://bucket/raw/US_Accidents_March23.csv
    output_path: str  # gs://bucket/processed/us_accidents
    min_severity: int = 3
    weather_conditions: list[str] = ["Rain", "Snow"]

    @field_validator("min_severity")
    @classmethod
    def severity_in_range(cls, v: int) -> int:
        if not (1 <= v <= 4):
            raise ValueError("min_severity must be between 1 and 4")
        return v


class MLConfig(BaseModel):
    train_ratio: float = 0.8
    num_trees: int = 50
    max_depth: int = 5
    model_path: str | None = None  # None → krok ML pominięty


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    spark: SparkConfig = SparkConfig()
    etl: ETLConfig
    ml: MLConfig = MLConfig()


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]

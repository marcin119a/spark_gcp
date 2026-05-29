from dataclasses import dataclass

from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import Imputer, StringIndexer, VectorAssembler
from pyspark.sql import DataFrame

from us_accidents_etl.config.settings import MLConfig

NUMERIC_FEATURES = [
    "Temperature(F)",
    "Humidity(%)",
    "Pressure(in)",
    "Visibility(mi)",
    "Wind_Speed(mph)",
    "Accident_Hour",
    "Accident_DayOfWeek",
    "Accident_Month",
    "Duration_Minutes",
]

CATEGORICAL_FEATURES = ["Weather_Condition", "Sunrise_Sunset", "State"]


@dataclass
class ModelMetrics:
    accuracy: float
    f1: float
    num_trees: int
    train_size: int
    test_size: int

    def __str__(self) -> str:
        return (
            f"accuracy={self.accuracy:.4f}  f1={self.f1:.4f}  "
            f"trees={self.num_trees}  train={self.train_size}  test={self.test_size}"
        )


def build_pipeline(cfg: MLConfig) -> Pipeline:
    indexers = [
        StringIndexer(inputCol=col, outputCol=f"{col}_idx", handleInvalid="keep")
        for col in CATEGORICAL_FEATURES
    ]

    imputer = Imputer(
        inputCols=NUMERIC_FEATURES,
        outputCols=[f"{c}_imp" for c in NUMERIC_FEATURES],
        strategy="median",
    )

    label_indexer = StringIndexer(
        inputCol="Severity", outputCol="label", handleInvalid="keep"
    )

    feature_cols = (
        [f"{c}_idx" for c in CATEGORICAL_FEATURES]
        + [f"{c}_imp" for c in NUMERIC_FEATURES]
    )
    assembler = VectorAssembler(
        inputCols=feature_cols, outputCol="features", handleInvalid="keep"
    )

    rf = RandomForestClassifier(
        featuresCol="features",
        labelCol="label",
        numTrees=cfg.num_trees,
        maxDepth=cfg.max_depth,
        seed=42,
    )

    return Pipeline(stages=[*indexers, imputer, label_indexer, assembler, rf])


def train(df: DataFrame, cfg: MLConfig) -> tuple[PipelineModel, ModelMetrics]:
    train_df, test_df = df.randomSplit(
        [cfg.train_ratio, 1.0 - cfg.train_ratio], seed=42
    )

    model = build_pipeline(cfg).fit(train_df)
    predictions = model.transform(test_df)

    def _eval(metric: str) -> float:
        return MulticlassClassificationEvaluator(metricName=metric).evaluate(predictions)

    metrics = ModelMetrics(
        accuracy=_eval("accuracy"),
        f1=_eval("f1"),
        num_trees=cfg.num_trees,
        train_size=train_df.count(),
        test_size=test_df.count(),
    )

    return model, metrics

"""Loads and detects databricks propierty commands for ide, jupyter and databricks. This can be referenced locally or from with notebooks (databricks or juptyer)
   Also loads the column_ext module extending pyspark.sql.column.Column. and JSONTypes for use across pipeline.
"""

import logging
from typing import Callable

import IPython as ip
import pyspark.sql.functions as F
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from pyspark.sql import DataFrame, SparkSession, SQLContext
from pyspark.sql.types import ArrayType, StructType

import project_pipeline.helpers.column_ext  # noqa: F401
from project_pipeline.private.json_type import JSONType, UnsafeJSONType   # noqa: F401


# check jupyter start dummy shell
if not ip.get_ipython():
    shell = TerminalInteractiveShell.instance()


# Logging
class SilenceFilter(logging.Filter):
    """Silience Filter.

    Args:
        logging ([type]): Filter Silence
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Overwrite logging.Filter method to silence it.

        Args:
            record (logging.LogRecord): the LoggingRecord to Silce.

        Returns:
            bool: False
        """
        return False


logging.basicConfig(format="%(asctime)s|%(levelname)s|%(name)s|%(message)s", level=logging.ERROR)
logging.getLogger("py4j.java_gateway").addFilter(SilenceFilter())
log = logging.getLogger("dbconnect")


def _check_is_databricks() -> bool:
    user_ns = ip.get_ipython().user_ns  # for jupyter
    return "displayHTML" in user_ns


def _get_spark() -> SparkSession:
    user_ns = ip.get_ipython().user_ns
    if "spark" in user_ns:
        return user_ns["spark"]
    else:
        spark = SparkSession.builder.getOrCreate()
        user_ns["spark"] = spark
        return spark


def _display(df: DataFrame) -> None:
    df.show(truncate=False)


def _display_with_json(df: DataFrame) -> None:
    for column in df.schema:
        t = type(column.dataType)
        if t == StructType or t == ArrayType:
            df = df.withColumn(column.name, F.to_json(column.name))
    df.show(truncate=False)


def _get_display() -> Callable[[DataFrame], None]:
    fn = ip.get_ipython().user_ns.get("display")
    return fn or _display_with_json


def _get_dbutils(spark: SparkSession):
    try:
        from pyspark.dbutils import DBUtils
        dbutils = DBUtils(spark)
    except ImportError:
        import IPython
        dbutils = IPython.get_ipython().user_ns.get("dbutils")
        if not dbutils:
            log.warning("could not initialise dbutils!")
    return dbutils


def _get_delta():
    if _check_is_databricks():
        from delta.tables import DeltaTable  # won't resolve locally.
    else:
        from deltalake import DeltaTable  # delta-lake-reader
    return DeltaTable


# initialise Spark variables
is_databricks: bool = _check_is_databricks()
spark: SparkSession = _get_spark()
display = _get_display()
dbutils = _get_dbutils(spark)
sc = spark.sparkContext
sqlContext = SQLContext(sc)
DeltaTable = _get_delta()

clusters: JSONType = {
    "dev": {
        "id": "--devclusterid--",
        "port": "8787"
    },
    "prod": {
        "id": "--prodclusterid--",
        "port": "8787"
    }
}


def use_cluster(cluster_name: str):
    """
    When running via Databricks Connect, specify to which cluster to connect instead of the default cluster.
    This call is ignored when running in Databricks environment.
    :param cluster_name: Name of the cluster as defined in the cluster array.
    """
    real_cluster_name = spark.conf.get("spark.databricks.clusterUsageTags.clusterName", None)

    # do not configure if we are already running in Databricks
    if not real_cluster_name:
        cluster_config = clusters.get(cluster_name)
        log.info(f"attaching to cluster '{cluster_name}' (id: {cluster_config['id']}, port: {cluster_config['port']})")

        spark.conf.set("spark.driver.host", "127.0.0.1")
        spark.conf.set("spark.databricks.service.clusterId", cluster_config["id"])
        spark.conf.set("spark.databricks.service.port", cluster_config["port"])

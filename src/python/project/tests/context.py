"""Set context to run unit tests in spark context."""
import os
import sys
import unittest
import logging
from project_pipeline.spark_context import spark


class PySparkTest(unittest.TestCase):

    @classmethod
    def suppress_py4j_logging(cls):
        logger = logging.getLogger("py4j")
        logger.setLevel(logging.WARN)

    @classmethod
    def create_testing_pyspark_session(cls):
        return (spark
        .master("local[2]")
        .appName("bp[tracking-testing-pyspark-context")
        .enableHiveSupport()
        .getOrCreate())

    @classmethod
    def setUpClass(cls):
        cls.suppress_py4j_logging()
        cls.spark = cls.create_testing_pyspark_session()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
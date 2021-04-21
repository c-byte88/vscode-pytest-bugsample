from datetime import datetime
import json
import uuid
import random
import string

from pyspark.sql.types import (
    ShortType,
    StringType,
    StructType,
    StructField,
    TimestampType,
    IntegerType
)
from pyspark.sql import DataFrame
from .context import spark


class SampleData():
    """ Class responsible for constructing DataFrames populated with test data """

    def __init__(self):
        self._spark = spark

    def sample1(self):
        schema = StructType(
            [
                StructField("id", IntegerType(), nullable=False),
                StructField("string", StringType(), nullable=False),
                StructField("nested", StructType(
                    [
                        StructField("nested_int", IntegerType(), nullable=True),
                        StructField("nested_string", StringType(), nullable=True)
                    ]
                ), nullable=False)
            ]
        )

        data = [(i, "foo"+str(i%20), [i, "foo"]) for i in range(1000)]

        return self._spark.createDataFrame(data, schema)

    def sample2(self, total_records):
        """ Generate JSON sample data """
        # TODO this needs expanding/completing
        # Will probably need to write files by constructing a dataframe and calling .save()
        # or using some other alternative to dbutils
        sample = {}
        letters = string.ascii_lowercase
        choice_1_list = ["a", "b", "c"]

        for i in range(total_records):
            new_uuid = str(uuid.uuid4())
            sample[new_uuid] = {}

            rand_str = ''.join(random.choice(letters) for i in range(10))
            choice_1 = choice_1_list[random.randint(0, len(choice_1_list)-1)]

            sample[new_uuid]['attr_1'] = rand_str
            sample[new_uuid]['attr_2'] = choice_1

        # return json.dumps(sample)
        return sample
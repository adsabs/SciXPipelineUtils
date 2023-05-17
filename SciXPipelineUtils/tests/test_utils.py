import logging
import os
from unittest import TestCase

import pytest
from confluent_kafka.schema_registry import Schema
from utils import get_schema, load_config

from SciXPipelineUtils.tests.mockschemaregistryclient import MockSchemaRegistryClient


class Logging:
    def __init__(self, logger):
        self.logger = logger


class test_utils_get_schema(TestCase):
    def test_get_schema(self):
        logger = Logging(logging)
        schema_client = MockSchemaRegistryClient()
        VALUE_SCHEMA_FILE = (
            "SciXPipelineUtils/tests/stubdata/AVRO_schemas/TEMPLATEInputSchema.avsc"
        )
        VALUE_SCHEMA_NAME = "TEMPLATEInputSchema"
        value_schema = open(VALUE_SCHEMA_FILE).read()

        schema_client.register(VALUE_SCHEMA_NAME, Schema(value_schema, "AVRO"))
        schema = get_schema(logger, schema_client, VALUE_SCHEMA_NAME)
        self.assertEqual(value_schema, schema)

    def test_get_schema_failure(self):
        logger = Logging(logging)
        schema_client = MockSchemaRegistryClient()
        with pytest.raises(Exception):
            get_schema(logger, schema_client, "FakeSchema")


class test_utils_get_config(TestCase):
    def test_load_config(self):
        config_path = "SciXPipelineUtils/tests/stubdata/"
        config_dict = {
            "PROJ_HOME": "/Users/sao/ADS_repos/backoffice/SciXPipelines/SciXPipelineUtils/SciXPipelineUtils/tests/stubdata",
            "AWS_ACCESS_KEY_ID": "CHANGEME",
            "AWS_BUCKET_ARN": "BUCKETARN",
            "AWS_BUCKET_NAME": "BUCKETNAME",
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_SECRET_ACCESS_KEY": "SECRETS",
            "KAFKA_BROKER": "kafka:9092",
            "LOGGING_LEVEL": "INFO",
            "LOG_STDOUT": True,
            "MINIO_ACCESS_KEY_ID": "admin",
            "MINIO_BUCKET_NAME": "scix-TEMPLATE",
            "MINIO_S3_URL": "http://minio:9000",
            "MINIO_SECRET_ACCESS_KEY": "supersecret",
            "PROFILE_NAME": "SESSION_PROFILE",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "S3_PROVIDERS": ["AWS", "MINIO"],
            "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
            "SQLALCHEMY_ECHO": False,
            "SQLALCHEMY_URL": "postgresql://template:TEMPLATE@localhost:5432/template",
            "TEMPLATE_INPUT_SCHEMA": "TEMPLATEInputSchema",
            "TEMPLATE_INPUT_TOPIC": "TEMPLATEInput",
            "TEMPLATE_OUTPUT_SCHEMA": "TEMPLATEOutputSchema",
            "TEMPLATE_OUTPUT_TOPIC": "TEMPLATEOutput",
        }
        config = load_config(config_path)
        self.assertEqual(config_dict, config)

    def test_load_config_path_does_not_exist(self):
        config_path = "SciXPipelineUtils/tests/stubdata/fake/"
        with pytest.raises(Exception):
            load_config(config_path)

    def test_load_config_from_env_vars(self):
        os.environ["AWS_ACCESS_KEY_ID"] = "new_key"
        config_path = "SciXPipelineUtils/tests/stubdata/"
        config_dict = {
            "PROJ_HOME": "/Users/sao/ADS_repos/backoffice/SciXPipelines/SciXPipelineUtils/SciXPipelineUtils/tests/stubdata",
            "AWS_ACCESS_KEY_ID": "CHANGEME",
            "AWS_BUCKET_ARN": "BUCKETARN",
            "AWS_BUCKET_NAME": "BUCKETNAME",
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_SECRET_ACCESS_KEY": "SECRETS",
            "KAFKA_BROKER": "kafka:9092",
            "LOGGING_LEVEL": "INFO",
            "LOG_STDOUT": True,
            "MINIO_ACCESS_KEY_ID": "admin",
            "MINIO_BUCKET_NAME": "scix-TEMPLATE",
            "MINIO_S3_URL": "http://minio:9000",
            "MINIO_SECRET_ACCESS_KEY": "supersecret",
            "PROFILE_NAME": "SESSION_PROFILE",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "S3_PROVIDERS": ["AWS", "MINIO"],
            "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
            "SQLALCHEMY_ECHO": False,
            "SQLALCHEMY_URL": "postgresql://template:TEMPLATE@localhost:5432/template",
            "TEMPLATE_INPUT_SCHEMA": "TEMPLATEInputSchema",
            "TEMPLATE_INPUT_TOPIC": "TEMPLATEInput",
            "TEMPLATE_OUTPUT_SCHEMA": "TEMPLATEOutputSchema",
            "TEMPLATE_OUTPUT_TOPIC": "TEMPLATEOutput",
        }

        config = load_config(config_path)
        self.assertNotEqual(config_dict, config)

        config_dict["AWS_ACCESS_KEY_ID"] = "new_key"
        self.assertEqual(config_dict, config)

        del os.environ["AWS_ACCESS_KEY_ID"]

        os.environ["S3_PROVIDERS"] = '{"Provider_1": "AWS"}'
        config_dict = {
            "PROJ_HOME": "/Users/sao/ADS_repos/backoffice/SciXPipelines/SciXPipelineUtils/SciXPipelineUtils/tests/stubdata",
            "AWS_ACCESS_KEY_ID": "CHANGEME",
            "AWS_BUCKET_ARN": "BUCKETARN",
            "AWS_BUCKET_NAME": "BUCKETNAME",
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_SECRET_ACCESS_KEY": "SECRETS",
            "KAFKA_BROKER": "kafka:9092",
            "LOGGING_LEVEL": "INFO",
            "LOG_STDOUT": True,
            "MINIO_ACCESS_KEY_ID": "admin",
            "MINIO_BUCKET_NAME": "scix-TEMPLATE",
            "MINIO_S3_URL": "http://minio:9000",
            "MINIO_SECRET_ACCESS_KEY": "supersecret",
            "PROFILE_NAME": "SESSION_PROFILE",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "S3_PROVIDERS": ["AWS", "MINIO"],
            "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
            "SQLALCHEMY_ECHO": False,
            "SQLALCHEMY_URL": "postgresql://template:TEMPLATE@localhost:5432/template",
            "TEMPLATE_INPUT_SCHEMA": "TEMPLATEInputSchema",
            "TEMPLATE_INPUT_TOPIC": "TEMPLATEInput",
            "TEMPLATE_OUTPUT_SCHEMA": "TEMPLATEOutputSchema",
            "TEMPLATE_OUTPUT_TOPIC": "TEMPLATEOutput",
        }

        config = load_config(config_path)
        print(config)

        self.assertNotEqual(config_dict, config)
        config_dict["S3_PROVIDERS"] = {"Provider_1": "AWS"}
        self.assertEqual(config_dict, config)

import datetime
import json
from unittest import TestCase

import avro
import avro_serializer
import pytest


class mock_gRPC_avro_msg:
    def value(self):
        return {
            "hash": "g425897fh3qp35890u54256342ewferht242546",
            "id": None,
            "task": "SYMBOL1",
            "status": None,
            "task_args": {
                "ingest": None,
                "ingest_type": "metadata",
                "daterange": "2023-03-07",
                "persistence": None,
            },
        }

    def resp_value(self):
        return {
            "record_id": "f5d9d314-67f3-4f9d-9c24-d46ab314f783",
            "record_sring": "<RECORD>",
            "s3_path": "pathfortesting",
            "task": "SYMBOL1",
            "datetime": datetime.datetime(1000, 1, 1, 0, 0, 0, 000000, tzinfo=avro.timezones.utc),
        }

    def bitstream(self):
        return b"\x00Ng425897fh3qp35890u54256342ewferht242546\x02\x00\x00\x00\x02\x10metadata\x02\x142023-03-07\x02"

    def resp_bitstream(self):
        return b"\x00Hf5d9d314-67f3-4f9d-9c24-d46ab314f783\x00\x10<RECORD>\x00\x1cpathfortesting\x00\xff\xaf\xb9\xf8\xdf\xf5\r"


class TestAvroSerializer(TestCase):
    def test_avro_serialization(self):
        with open("tests/stubdata/AVRO_schemas/TEMPLATEInputSchema.avsc") as f:
            schema_json = json.load(f)
        msg = mock_gRPC_avro_msg().value()
        serializer = avro_serializer.AvroSerialHelper(json.dumps(schema_json))
        bitstream = serializer.avro_serializer(msg)
        self.assertEqual(bitstream, mock_gRPC_avro_msg().bitstream())

    def test_avro_serialization_failure(self):
        with open("tests/stubdata/AVRO_schemas/TEMPLATEInputSchema.avsc") as f:
            schema_json = json.load(f)
        msg = {}
        serializer = avro_serializer.AvroSerialHelper(json.dumps(schema_json))
        with pytest.raises(avro.errors.AvroTypeException):
            serializer.avro_serializer(msg)

    def test_avro_deserialization(self):
        with open("tests/stubdata/AVRO_schemas/TEMPLATEInputSchema.avsc") as f:
            schema_json = json.load(f)
        serializer = avro_serializer.AvroSerialHelper(json.dumps(schema_json))
        bitstream = mock_gRPC_avro_msg().bitstream()
        msg = serializer.avro_deserializer(bitstream)
        self.assertEqual(msg, mock_gRPC_avro_msg().value())

    def test_avro_deserialization_failure(self):
        with open("tests/stubdata/AVRO_schemas/TEMPLATEInputSchema.avsc") as f:
            schema_json = json.load(f)
        serializer = avro_serializer.AvroSerialHelper(json.dumps(schema_json))
        bitstream = b""
        with pytest.raises(Exception):
            serializer.avro_deserializer(bitstream)

    def test_avro_serialization_deserialization_seperate_schema(self):
        with open("tests/stubdata/AVRO_schemas/TEMPLATEInputSchema.avsc") as f:
            req_schema_json = json.load(f)
        with open("tests/stubdata/AVRO_schemas/TEMPLATEOutputSchema.avsc") as f:
            res_schema_json = json.load(f)

        msg = mock_gRPC_avro_msg().value()
        serializer = avro_serializer.AvroSerialHelper(
            ser_schema=json.dumps(req_schema_json), des_schema=json.dumps(res_schema_json)
        )
        bitstream = serializer.avro_serializer(msg)
        self.assertEqual(bitstream, mock_gRPC_avro_msg().bitstream())

        bitstream = mock_gRPC_avro_msg().resp_bitstream()
        msg = serializer.avro_deserializer(bitstream)
        self.assertEqual(msg, mock_gRPC_avro_msg().resp_value())

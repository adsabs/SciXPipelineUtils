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

    def bitstream(self):
        return b"\x00Ng425897fh3qp35890u54256342ewferht242546\x02\x00\x00\x00\x02\x10metadata\x02\x142023-03-07\x02"


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

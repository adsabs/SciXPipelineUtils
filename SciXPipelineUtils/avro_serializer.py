import io

import avro.io
import avro.schema
from avro.schema import parse


class AvroSerialHelper:
    def __init__(self, ser_schema, des_schema=None, logger=None):
        """
        :param schema: The AVRO schema (str)
        :param logger: Application logger
        """
        self.ser_schema = parse(ser_schema)
        self.des_schema = parse(ser_schema)

        if des_schema:
            self.des_schema = parse(des_schema)

        self.logger = logger

    def avro_serializer(self, msg):
        """
        :param msg: the json representation of the AVRO message
        :return: serialized message (bitstream)
        """
        writer = avro.io.DatumWriter(self.ser_schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        try:
            writer.write(msg, encoder)
            return bytes_writer.getvalue()

        except avro.errors.AvroTypeException as e:
            print("Failed to serialize request with error: {} \nStopping.".format(e))
            raise e

    def avro_deserializer(self, raw_bytes):
        """
        :param raw_bytes: The raw bitstream of an incoming AVRO message
        :returns: The json representation of the AVRO message
        """
        if self.logger:
            self.logger.debug(raw_bytes)
        bytes_reader = io.BytesIO(raw_bytes)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(self.des_schema)
        try:
            return reader.read(decoder)
        except Exception as e:
            if self.logger:
                self.logger.exception(e)
            raise e

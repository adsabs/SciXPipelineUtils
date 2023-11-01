import uuid
from unittest import TestCase

from scix_uuid import scix_uuid


class TestSciXUUIDImplementation(TestCase):
    def test_generate_uuid7(self):
        test_uuid = scix_uuid.uuid7()
        self.assertEqual(type(test_uuid), uuid.UUID)
        self.assertEqual(type(test_uuid.hex), str)
        self.assertEqual(len(test_uuid.bytes), 16)

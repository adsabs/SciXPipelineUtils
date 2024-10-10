from unittest import TestCase

import SciXPipelineUtils.scix_id as scixid


class TestSciXUUIDImplementation(TestCase):
    def test_generate_uuid7(self):
        test_id = scixid.encode(1000)
        self.assertEqual(test_id, "0000-0000-0Z81")
        test_int = scixid.decode(test_id)
        self.assertEqual(test_int, 1000)

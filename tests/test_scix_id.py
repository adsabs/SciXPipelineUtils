from unittest import TestCase

import SciXPipelineUtils.scix_id as scixid


class TestSciXIDImplementation(TestCase):
    def test_generate_scixid(self):
        test_id = scixid.encode(1000)
        self.assertEqual(test_id, "0000-0000-0Z8A")
        test_int = scixid.decode(test_id)
        self.assertEqual(test_int, 1000)

    def test_generate_scixid_no_checksum(self):
        test_id = scixid.encode(1000, checksum=False)
        self.assertEqual(test_id, "0000-0000-00Z8")
        test_int = scixid.decode(test_id, checksum=False)
        self.assertEqual(test_int, 1000)

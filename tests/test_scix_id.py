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

    def test_generate_bib_data_hash(self):
        test_bib_data = {
            "id": 1,
            "author": ["Lias, Alberta", "Smith, J."],
            "title": "Test",
            "abs": "words",
            "bibcode": "Test",
        }
        hash = scixid.generate_bib_data_hash(test_bib_data)
        self.assertEqual(hash, "ca77650a961fe043bf18e60618f43b49")

        test_bib_data = {
            "title": "Test",
            "abs": "words",
        }
        hash2 = scixid.generate_bib_data_hash(test_bib_data)
        self.assertEqual(hash2, "ca77650a961fe043bf18e60618f43b49")

        self.assertEqual(hash, hash2)

    def test_get_rand_from_hash(self):
        test_bib_data = {
            "id": 1,
            "author": ["Lias, Alberta", "Smith, J."],
            "title": "Test",
            "abs": "words",
        }
        hash = scixid.generate_bib_data_hash(test_bib_data)
        rand_num = scixid.get_rand_from_hash(hash)
        self.assertEqual(rand_num, 12446194448305896)

    def test_scix_id_from_hash(self):
        test_bib_data = {
            "id": 1,
            "author": ["Lias, Alberta", "Smith, J."],
            "title": "Test",
            "abs": "words",
        }
        hash = scixid.generate_bib_data_hash(test_bib_data)
        scix_id = scixid.scix_id_from_hash(hash)
        self.assertEqual(scix_id, "B1QQ-XVEB-3Q83")

    def test_generate_scix_id(self):
        test_bib_data = {
            "id": 1,
            "author": ["Lias, Alberta", "Smith, J."],
            "title": "Test",
            "abs": "words",
        }
        scix_id = scixid.generate_scix_id(test_bib_data)
        self.assertEqual(scix_id, "B1QQ-XVEB-3Q83")

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
            "authors": ["Lias, Alberta", "Smith, J."],
            "title": "Test",
            "abs": "words",
        }
        hash = scixid.generate_bib_data_hash(test_bib_data)
        self.assertEqual(hash, "7a58d48ab6931dafc48066153eb3ef79")

    def test_get_rand_from_hash(self):
        test_bib_data = {
            "id": 1,
            "authors": ["Lias, Alberta", "Smith, J."],
            "title": "Test",
            "abs": "words",
        }
        hash = scixid.generate_bib_data_hash(test_bib_data)
        rand_num = scixid.get_rand_from_hash(hash)
        self.assertEqual(rand_num, 11501195142287729)

    def test_scix_id_from_hash(self):
        test_bib_data = {
            "id": 1,
            "authors": ["Lias, Alberta", "Smith, J."],
            "title": "Test",
            "abs": "words",
        }
        hash = scixid.generate_bib_data_hash(test_bib_data)
        scix_id = scixid.scix_id_from_hash(hash)
        self.assertEqual(scix_id, "A6W8-TNF5-MBHU")

    def test_generate_scix_id(self):
        test_bib_data = {
            "id": 1,
            "authors": ["Lias, Alberta", "Smith, J."],
            "title": "Test",
            "abs": "words",
        }
        scix_id = scixid.generate_scix_id(test_bib_data)
        self.assertEqual(scix_id, "A6W8-TNF5-MBHU")

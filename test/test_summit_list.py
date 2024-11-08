import unittest
import os

from summit import summit_list


class TestSummitList(unittest.TestCase):
    def setUp(self):
        self.test_file_path = os.path.join(os.path.dirname(__file__), "100cims.csv")
        return super().setUp()

    def test_read_from_file(self):
        summits = summit_list.load_from_file(self.test_file_path)

        self.assertEqual(len(summits._summits), 150)

    def test_parse_coordinates(self):
        summits = summit_list.load_from_file(self.test_file_path)
        expected_coords = (42.07611111, 2.40722222)
        parsed_coords = summits._parse_coordinates_text("42° 04′ 34″ N, 2° 24′ 26″ E")
        self.assertAlmostEqual(expected_coords[0], parsed_coords[0])
        self.assertAlmostEqual(expected_coords[1], parsed_coords[1])

        self.assertTrue("Coordinates" in summits._summits)

    def test_get_closest(self):
        summits = summit_list.load_from_file(self.test_file_path)
        response = summits.get_closest_summits("Montseny")

        self.assertEqual(len(response), 5)

        self.assertEqual(response.iloc[0]["Nom"], "les Agudes")
        self.assertEqual(response.iloc[1]["Nom"], "Matagalls")
        self.assertEqual(response.iloc[2]["Nom"], "Turó de Tagamanent")

    def test_get_closest_str(self):
        summits = summit_list.load_from_file(self.test_file_path)
        response = summits.get_closest_summits("Montseny", limit_num=3)

        response_str = summit_list.message_from_df(response)

        expected_response = """les Agudes (1705m) a 5.2 km\nMatagalls (1697m) a 5.6 km\nTuró de Tagamanent (1056m) a 8.3 km"""
        self.assertEqual(response_str, expected_response)

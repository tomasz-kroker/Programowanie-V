import unittest
import tempfile
from pathlib import Path

import pandas as pd

from data_cleaning import DataSession
from data_profile import generate_profile, count_duplicates


class TestDataQuality(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Wiek": [10.0, 20.0, 20.0, None, -5.0],
            "Region": ["north", "south", "south", None, "north"]
        })

        self.session = DataSession(self.df)

    def test_profile(self):
        profile = generate_profile(self.df)

        self.assertEqual(profile.loc["Wiek", "Braki"], 1)
        self.assertEqual(profile.loc["Region", "Braki"], 1)
        self.assertEqual(profile.loc["Wiek", "Unikalne wartości"], 3)

    def test_duplicates(self):
        df = pd.DataFrame({
            "A": [1, 2, 2, 3],
            "B": ["a", "b", "b", "c"]
        })

        session = DataSession(df)

        removed = session.remove_duplicates()

        self.assertEqual(removed, 1)
        self.assertEqual(len(session.current), 3)
        self.assertEqual(count_duplicates(session.current), 0)

    def test_fill_missing_median(self):
        filled = self.session.fill_missing("Wiek", "mediana")

        self.assertEqual(filled, 1)
        self.assertEqual(self.session.current["Wiek"].isna().sum(), 0)
        self.assertEqual(self.session.current.loc[3, "Wiek"], 15.0)

    def test_fill_missing_mode(self):
        filled = self.session.fill_missing("Region", "dominanta")

        self.assertEqual(filled, 1)
        self.assertEqual(self.session.current.loc[3, "Region"], "north")

    def test_drop_missing(self):
        removed = self.session.drop_missing("Wiek")

        self.assertEqual(removed, 1)
        self.assertEqual(len(self.session.current), 4)

    def test_invalid_range(self):
        mask = self.session.invalid_range_mask(
            "Wiek",
            minimum=0,
            maximum=52
        )

        self.assertEqual(int(mask.sum()), 1)

        corrected = self.session.replace_invalid_with_missing(
            "Wiek",
            minimum=0,
            maximum=52
        )

        self.assertEqual(corrected, 1)
        self.assertTrue(pd.isna(self.session.current.loc[4, "Wiek"]))

    def test_iqr(self):
        df = pd.DataFrame({
            "Wartosc": [1, 2, 3, 4, 5, 100]
        })

        session = DataSession(df)

        mask = session.iqr_mask("Wartosc")

        self.assertEqual(int(mask.sum()), 1)
        self.assertTrue(bool(mask.iloc[5]))

    def test_mark_outliers(self):
        df = pd.DataFrame({
            "Wartosc": [1, 2, 3, 4, 5, 100]
        })

        session = DataSession(df)

        marked = session.mark_outliers_iqr("Wartosc")

        self.assertEqual(marked, 1)
        self.assertIn("Wartosc_outlier", session.current.columns)
        self.assertEqual(len(session.current), 6)

    def test_reset(self):
        self.session.drop_missing("Wiek")
        self.session.reset()

        pd.testing.assert_frame_equal(
            self.session.current,
            self.df
        )

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            self.session.invalid_range_mask(
                "Wiek",
                minimum=100,
                maximum=10
            )

        with self.assertRaises(ValueError):
            self.session.iqr_mask("Wiek", factor=-1)

        with self.assertRaises(ValueError):
            self.session.fill_missing("Region", "mediana")

    def test_original_data_unchanged(self):
        self.session.fill_missing("Wiek", "mediana")

        pd.testing.assert_frame_equal(
            self.session.raw,
            self.df
        )

    def test_csv_export_import(self):
        df = pd.DataFrame({
            "Wiek": [10, 20, 30],
            "Region": ["north", "south", "north"]
        })

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "cleaned.csv"

            df.to_csv(
                path,
                sep=";",
                index=False,
                encoding="utf-8-sig"
            )

            loaded = pd.read_csv(path, sep=";")

            pd.testing.assert_frame_equal(df, loaded)


if __name__ == "__main__":
    unittest.main()
import unittest
import json
import csv
import tempfile
from pathlib import Path

from converters.csv_json import csv_to_json, json_to_csv


class TestCsvJson(unittest.TestCase):

    def test_csv_to_json(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "test.csv"
            destination = Path(folder) / "test.json"

            source.write_text(
                "imie,miasto\nJan,Opole\nAnna,Gogolin\n",
                encoding="utf-8"
            )

            csv_to_json(source, destination)

            with destination.open(encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["imie"], "Jan")
            self.assertEqual(data[1]["miasto"], "Gogolin")

    def test_json_to_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "test.json"
            destination = Path(folder) / "test.csv"

            source.write_text(
                '[{"imie": "Jan", "miasto": "Opole"}]',
                encoding="utf-8"
            )

            json_to_csv(source, destination)

            with destination.open(
                encoding="utf-8", newline=""
            ) as file:
                data = list(csv.DictReader(file))

            self.assertEqual(data[0]["imie"], "Jan")
            self.assertEqual(data[0]["miasto"], "Opole")

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "bledny.json"
            destination = Path(folder) / "wynik.csv"

            source.write_text(
                "{to nie jest poprawny JSON}",
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                json_to_csv(source, destination)


if __name__ == "__main__":
    unittest.main()

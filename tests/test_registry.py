import unittest
import tempfile
from pathlib import Path

from converters.registry import available_targets, execute


class TestRegistry(unittest.TestCase):

    def test_available_targets(self):

        self.assertEqual(
            available_targets(Path("test.docx")),
            [".pdf", ".txt"]
        )

        self.assertEqual(
            available_targets(Path("test.csv")),
            [".json"]
        )

        self.assertEqual(
            available_targets(Path("test.odt")),
            [".pdf"]
        )

    def test_unsupported_conversion(self):


        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "test.csv"
            destination = Path(folder) / "test.pdf"

            source.write_text(
                "imie\nJan\n",
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                execute(source, destination)

    def test_missing_source(self):

        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "brak.csv"
            destination = Path(folder) / "wynik.json"

            with self.assertRaises(FileNotFoundError):
                execute(source, destination)

    def test_existing_destination(self):

        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "test.csv"
            destination = Path(folder) / "test.json"

            source.write_text(
                "imie\nJan\n",
                encoding="utf-8"
            )

            destination.write_text(
                "Istniejacy plik",
                encoding="utf-8"
            )

            with self.assertRaises(FileExistsError):
                execute(source, destination)

            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                "Istniejacy plik"
            )


if __name__ == "__main__":
    unittest.main()

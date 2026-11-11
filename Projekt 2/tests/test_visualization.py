import unittest
from io import BytesIO

import pandas as pd
from matplotlib.figure import Figure

from data_visualization import (
    create_plot,
    calculate_correlation
)


class TestVisualization(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Wiek": [20, 30, 40, 60],
            "Dochod": [2, 3, 5, 7],
            "Region": ["north", "south", "north", "south"],
            "Stala": [1, 1, 1, 1]
        })

    def test_histogram(self):
        fig = create_plot(
            self.df, "histogram", "Wiek"
        )

        self.assertIsInstance(fig, Figure)
        self.assertEqual(fig.axes[0].get_xlabel(), "Wiek")

    def test_scatter(self):
        fig = create_plot(
            self.df, "scatter", "Wiek", "Dochod"
        )

        self.assertIsInstance(fig, Figure)
        self.assertEqual(fig.axes[0].get_ylabel(), "Dochod")

    def test_box(self):
        fig = create_plot(
            self.df, "box", "Wiek"
        )

        self.assertIsInstance(fig, Figure)

    def test_bar(self):
        fig = create_plot(
            self.df, "bar", "Region", "Dochod"
        )

        self.assertIsInstance(fig, Figure)
        self.assertEqual(fig.axes[0].get_xlabel(), "Region")

    def test_correlation(self):
        df = pd.DataFrame({
            "X": [1, 2, 3, 4],
            "Y": [3, 6, 9, 12]
        })

        result = calculate_correlation(df, "X", "Y")

        self.assertAlmostEqual(result, 1.0)

    def test_export_formats(self):
        fig = create_plot(
            self.df, "histogram", "Wiek"
        )

        for extension in ("png", "pdf", "svg"):
            with self.subTest(format=extension):
                buffer = BytesIO()

                fig.savefig(
                    buffer,
                    format=extension
                )

                content = buffer.getvalue()

                self.assertGreater(len(content), 0)

                if extension == "png":
                    self.assertTrue(
                        content.startswith(b"\x89PNG")
                    )

                elif extension == "pdf":
                    self.assertTrue(
                        content.startswith(b"%PDF-")
                    )

                elif extension == "svg":
                    self.assertIn(b"<svg", content)

                buffer.close()

    def test_histogram_text_error(self):
        with self.assertRaises(ValueError):
            create_plot(
                self.df, "histogram", "Region"
            )

    def test_scatter_no_y_error(self):
        with self.assertRaises(ValueError):
            create_plot(
                self.df, "scatter", "Wiek"
            )

    def test_scatter_same_column_error(self):
        with self.assertRaises(ValueError):
            create_plot(
                self.df, "scatter", "Wiek", "Wiek"
            )

    def test_bar_numeric_x_error(self):
        with self.assertRaises(ValueError):
            create_plot(
                self.df, "bar", "Wiek", "Dochod"
            )

    def test_constant_column_error(self):
        with self.assertRaises(ValueError):
            create_plot(
                self.df, "histogram", "Stala"
            )

    def test_unknown_chart_error(self):
        with self.assertRaises(ValueError):
            create_plot(
                self.df, "nieznany", "Wiek"
            )

    def test_missing_column_error(self):
        with self.assertRaises(ValueError):
            create_plot(
                self.df, "histogram", "NieIstnieje"
            )

    def test_empty_dataframe_error(self):
        empty_df = self.df.iloc[0:0]

        with self.assertRaises(ValueError):
            create_plot(
                empty_df, "histogram", "Wiek"
            )


if __name__ == "__main__":
    unittest.main()
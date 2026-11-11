import pandas as pd
import seaborn as sns

from matplotlib.figure import Figure
from pandas.api.types import is_numeric_dtype


def validate_numeric(df, column):
    if column not in df.columns:
        raise ValueError(f"Nie znaleziono kolumny: {column}")

    if not is_numeric_dtype(df[column]):
        raise ValueError(
            f"Kolumna {column} musi byc liczbowa."
        )

    if df[column].dropna().nunique() < 2:
        raise ValueError(
            f"Kolumna {column} nie zawiera wystarczajaco roznych wartosci."
        )


def create_plot(df, chart_type, x, y=None, title=None):
    if df.empty:
        raise ValueError("Zbior danych jest pusty.")

    if x not in df.columns:
        raise ValueError(f"Nie znaleziono kolumny: {x}")

    fig = Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)

    if chart_type == "histogram":
        validate_numeric(df, x)

        sns.histplot(
            data=df,
            x=x,
            bins=30,
            ax=ax
        )

        ax.set_xlabel(x)
        ax.set_ylabel("Liczba rekordow")

    elif chart_type == "scatter":
        if y is None:
            raise ValueError("Wybierz kolumne Y.")

        validate_numeric(df, x)
        validate_numeric(df, y)

        if x == y:
            raise ValueError("Wybierz dwie rozne kolumny.")

        data = df[[x, y]].dropna()

        if len(data) < 2:
            raise ValueError("Za malo poprawnych obserwacji.")

        sns.scatterplot(
            data=data,
            x=x,
            y=y,
            ax=ax,
            alpha=0.5,
            s=15
        )

        ax.set_xlabel(x)
        ax.set_ylabel(y)

    elif chart_type == "box":
        validate_numeric(df, x)

        sns.boxplot(
            data=df,
            x=x,
            ax=ax
        )

        ax.set_xlabel(x)
        ax.set_ylabel("")

    elif chart_type == "bar":
        if y is None:
            raise ValueError("Wybierz kolumne Y.")

        if is_numeric_dtype(df[x]):
            raise ValueError(
                "Kolumna X musi byc kategoryczna."
            )

        validate_numeric(df, y)

        if df[x].nunique() > 20:
            raise ValueError(
                "Za duzo kategorii do wykresu slupkowego."
            )

        data = df[[x, y]].copy()
        data[x] = data[x].astype("string").fillna("Brak danych")
        data = data.dropna(subset=[y])

        grouped = data.groupby(
            x,
            as_index=False
        )[y].mean()

        ax.bar(
            grouped[x].astype(str),
            grouped[y]
        )

        ax.set_xlabel(x)
        ax.set_ylabel(f"Srednia wartosc: {y}")

    else:
        raise ValueError("Nieznany typ wykresu.")

    if title is None:
        title = f"{chart_type}: {x}"

    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    return fig


def calculate_correlation(df, column_x, column_y):
    validate_numeric(df, column_x)
    validate_numeric(df, column_y)

    data = df[[column_x, column_y]].dropna()

    if len(data) < 2:
        raise ValueError("Za malo danych do korelacji.")

    return data[column_x].corr(data[column_y])
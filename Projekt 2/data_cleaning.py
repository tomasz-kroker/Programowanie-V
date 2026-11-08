from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd
from pandas.api.types import is_numeric_dtype


@dataclass
class DataSession:
    raw: pd.DataFrame
    current: pd.DataFrame = field(init=False)
    audit_log: list = field(default_factory=list)

    def __post_init__(self):
        self.raw = self.raw.copy(deep=True)
        self.current = self.raw.copy(deep=True)

    def add_log(self, operation, parameters, before, affected):
        self.audit_log.append({
            "Czas": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Operacja": operation,
            "Parametry": parameters,
            "Rekordy przed": before,
            "Rekordy po": len(self.current),
            "Rekordy dotkniete": affected
        })

    def remove_duplicates(self):
        before = len(self.current)

        self.current = self.current.drop_duplicates().copy()

        removed = before - len(self.current)

        self.add_log(
            "Usuwanie duplikatow",
            "Pelne duplikaty",
            before,
            removed
        )

        return removed

    def drop_missing(self, column):
        if column not in self.current.columns:
            raise ValueError("Nie znaleziono kolumny.")

        before = len(self.current)

        self.current = self.current.dropna(
            subset=[column]
        ).copy()

        removed = before - len(self.current)

        self.add_log(
            "Usuwanie brakow",
            column,
            before,
            removed
        )

        return removed

    def fill_missing(self, column, strategy):
        if column not in self.current.columns:
            raise ValueError("Nie znaleziono kolumny.")

        before = len(self.current)
        missing = int(self.current[column].isna().sum())

        if strategy == "mediana":
            if not is_numeric_dtype(self.current[column]):
                raise ValueError(
                    "Mediana wymaga kolumny liczbowej."
                )

            value = self.current[column].median()

        elif strategy == "dominanta":
            modes = self.current[column].mode(dropna=True)

            if modes.empty:
                raise ValueError(
                    "Brak wartości do uzupełnienia."
                )

            value = modes.iloc[0]

        else:
            raise ValueError("Nieznana strategia.")

        if pd.isna(value):
            raise ValueError(
                "Nie można obliczyć wartości zastępczej."
            )

        self.current[column] = (
            self.current[column].fillna(value)
        )

        self.add_log(
            "Uzupelnianie brakow",
            f"{column}, {strategy}, wartosc={value}",
            before,
            missing
        )

        return missing

    def reset(self):
        before = len(self.current)

        self.current = self.raw.copy(deep=True)

        self.add_log(
            "Przywracanie danych",
            "Dane oryginalne",
            before,
            len(self.raw)
        )
        
    def invalid_range_mask(self, column, minimum=None, maximum=None):
        if column not in self.current.columns:
            raise ValueError("Nie znaleziono kolumny.")

        if not is_numeric_dtype(self.current[column]):
            raise ValueError("Regula zakresu wymaga kolumny liczbowej.")

        if minimum is None and maximum is None:
            raise ValueError("Podaj minimum lub maksimum.")

        if minimum is not None and maximum is not None:
            if minimum > maximum:
                raise ValueError("Minimum nie moze byc wieksze od maksimum.")

        values = self.current[column]
        mask = pd.Series(False, index=self.current.index)

        if minimum is not None:
            mask = mask | (values < minimum)

        if maximum is not None:
            mask = mask | (values > maximum)

        return mask.fillna(False)


    def replace_invalid_with_missing(self, column, minimum=None, maximum=None):
        mask = self.invalid_range_mask(column, minimum, maximum)

        before = len(self.current)
        affected = int(mask.sum())

        self.current.loc[mask, column] = float("nan")

        self.add_log(
            "Korekta zakresu",
            f"{column}, zakres={minimum} do {maximum}, zamiana na NaN",
            before,
            affected
        )

        return affected


    def iqr_mask(self, column, factor=1.5):
        if column not in self.current.columns:
            raise ValueError("Nie znaleziono kolumny.")

        if not is_numeric_dtype(self.current[column]):
            raise ValueError("Metoda IQR wymaga kolumny liczbowej.")

        if factor <= 0:
            raise ValueError("Wspolczynnik IQR musi byc dodatni.")

        values = self.current[column]

        if values.dropna().empty:
            raise ValueError("Kolumna nie zawiera danych liczbowych.")

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            return pd.Series(False, index=self.current.index)

        lower = q1 - factor * iqr
        upper = q3 + factor * iqr

        return ((values < lower) | (values > upper)).fillna(False)


    def mark_outliers_iqr(self, column, factor=1.5):
        mask = self.iqr_mask(column, factor)

        before = len(self.current)
        affected = int(mask.sum())

        new_column = f"{column}_outlier"

        self.current[new_column] = mask

        self.add_log(
            "Oznaczanie outlierow",
            f"{column}, IQR={factor}, flaga={new_column}",
            before,
            affected
        )

        return affected
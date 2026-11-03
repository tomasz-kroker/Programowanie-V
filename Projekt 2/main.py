from pathlib import Path
import pandas as pd

# Ścieżka do pliku CSV
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "data" / "california_housing_z_problemami.csv"

# Wczytanie danych
try:
    df = pd.read_csv(file_path, sep=None, engine="python")

    if df.empty:
        raise ValueError("Plik nie zawiera rekordów.")

    print("=== PODGLĄD DANYCH ===")
    print(df.head())

    print("\n=== INFORMACJE O ZBIORZE ===")
    print("Liczba rekordów:", len(df))
    print("Liczba kolumn:", len(df.columns))

    print("\n=== TYPY KOLUMN ===")
    print(df.dtypes)

    print("\n=== BRAKUJĄCE WARTOŚCI ===")
    print(df.isnull().sum())

    print("\n=== DUPLIKATY ===")
    print("Liczba duplikatów:", df.duplicated().sum())

    print("\n=== STATYSTYKI OPISOWE ===")
    print(df.describe(include="all"))

except (FileNotFoundError, UnicodeError, pd.errors.ParserError, ValueError) as e:
    print("Błąd wczytywania danych:", e)

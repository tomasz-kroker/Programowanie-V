from pathlib import Path
import pandas as pd

from data_profile import generate_profile, generate_statistics
from data_cleaning import DataSession


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

file_path = DATA_DIR / "california_housing_z_problemami.csv"

try:

    df = pd.read_csv(file_path, sep=None, engine="python")

    if df.empty:
        raise ValueError("Plik nie zawiera rekordow.")

    session = DataSession(df)

    print("=== DANE PRZED CZYSZCZENIEM ===")
    print("Liczba rekordow:", len(session.current))
    print("Liczba duplikatow:", session.current.duplicated().sum())
    print("Liczba brakow:", session.current.isna().sum().sum())

    profile_before = generate_profile(session.current)

    profile_before.to_csv(
        REPORT_DIR / "profil_przed.csv",
        sep=";",
        encoding="utf-8-sig",
        index_label="Kolumna"
    )

    removed = session.remove_duplicates()
    print("\nUsunieto duplikatow:", removed)

    filled_medinc = session.fill_missing("MedInc", "mediana")
    print("Uzupelniono MedInc:", filled_medinc)

    filled_region = session.fill_missing("Region", "dominanta")
    print("Uzupelniono Region:", filled_region)


    invalid = session.invalid_range_mask(
        "HouseAge",
        minimum=0,
        maximum=52
    )

    print("\n=== KONTROLA ZAKRESU ===")
    print("Nieprawidlowe wartosci HouseAge:", int(invalid.sum()))

    corrected = session.replace_invalid_with_missing(
        "HouseAge",
        minimum=0,
        maximum=52
    )

    print("Oznaczono jako brak:", corrected)

    filled_age = session.fill_missing("HouseAge", "mediana")
    print("Uzupelniono HouseAge:", filled_age)

    print("\n=== WARTOSCI ODSTAJACE ===")

    outliers = session.mark_outliers_iqr(
        "AveRooms",
        factor=1.5
    )

    print("Wykryto outlierow AveRooms:", outliers)
    print("Dodano kolumne AveRooms_outlier")

    profile_after = generate_profile(session.current)

    profile_after.to_csv(
        REPORT_DIR / "profil_po.csv",
        sep=";",
        encoding="utf-8-sig",
        index_label="Kolumna"
    )

    session.current.to_csv(
        REPORT_DIR / "cleaned.csv",
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    history = pd.DataFrame(session.audit_log)

    history.to_csv(
        REPORT_DIR / "historia_zmian.csv",
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n=== DANE PO CZYSZCZENIU ===")
    print("Liczba rekordow:", len(session.current))
    print("Liczba duplikatow:", session.current.duplicated().sum())
    print("Liczba brakow:", session.current.isna().sum().sum())

    print("\n=== HISTORIA ZMIAN ===")
    print(history.to_string(index=False))

    print("\n=== ZAPISANO PLIKI ===")
    print("profil_przed.csv")
    print("profil_po.csv")
    print("cleaned.csv")
    print("historia_zmian.csv")

except (
    FileNotFoundError,
    UnicodeError,
    pd.errors.ParserError,
    ValueError,
    OSError
) as e:
    print("Blad:", e)

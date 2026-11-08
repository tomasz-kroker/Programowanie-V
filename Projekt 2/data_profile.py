import pandas as pd

def generate_profile(df):
    profile = pd.DataFrame({
        "Typ danych": df.dtypes.astype(str),
        "Braki": df.isnull().sum(),
        "Braki (%)": (df.isnull().mean() * 100).round(2),
        "Unikalne wartości": df.nunique()
    })

    return profile


def generate_statistics(df):
    return df.describe(include="all")


def count_duplicates(df):
    return df.duplicated().sum()

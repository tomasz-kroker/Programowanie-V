# Projekt 2 — materiały pomocnicze

Pakiet do instrukcji **Programowanie V – Projekt 2: Studio jakości i wizualizacji danych**. Materiały nie zawierają rozwiązania aplikacji.

## Co jest w pakiecie

- `generate_reference.py` — generuje rzeczywisty California Housing z **celowo dodanymi błędami**.
- `test_01`…`test_06` — małe pliki do weryfikacji importu, profilowania, czyszczenia i walidacji wykresów.
- `OCZEKIWANE_WYNIKI.md` — zestaw wyników do sprawdzenia.
- `requirements_materialy.txt` — zależności potrzebne **wyłącznie do generatora**.

## Przygotowanie zbioru referencyjnego (prowadzący)

```bash
python -m pip install -r requirements_materialy.txt
python generate_reference.py
```

Pierwsze uruchomienie wymaga dostępu do internetu. Powstaną `california_housing_z_problemami.csv` i `manifest_referencyjny.json`. Następnie prowadzący udostępnia **ten sam wynikowy CSV** wszystkim studentom. Wersję generatora i wynikowy plik warto zachować wraz z materiałami kursu. `scikit-learn` jest potrzebny do pobrania zbioru, **nie jest wymaganym składnikiem aplikacji studenta**.

Dane California Housing pochodzą z danych spisowych USA z 1990 r., dostarczanych przez scikit-learn; nie zawierają braków w oryginalnej wersji. Wartości skrajne w oryginalnym zbiorze mogą być realnymi obserwacjami. Syntetyczne błędy wprowadzone skryptem nie powinny być uznawane za wiarygodne dane ekonomiczne.

## Dokumentacja

- [California Housing — scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html)
- [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Matplotlib — Embed in Tk](https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html)
- [Seaborn — Tutorial](https://seaborn.pydata.org/tutorial.html)

Biblioteki studenckiej aplikacji powinny być opisane w jej własnym `requirements.txt`. Tkinter często jest dołączony do Pythona, ale na niektórych dystrybucjach Linux wymaga instalacji pakietu systemowego (np. `python3-tk`).

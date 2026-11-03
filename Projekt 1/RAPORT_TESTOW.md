# Raport testów – Uniwersalny konwerter plików

## 1. Cel testowania

Celem testów było sprawdzenie poprawności działania aplikacji umożliwiającej konwersję plików CSV, JSON, TXT, DOCX, ODT i PDF.

Weryfikowano poprawność konwersji, zachowanie polskich znaków, obsługę błędnych danych, działanie interfejsu graficznego oraz bezpieczeństwo zapisu plików.

## 2. Środowisko testowe

- System operacyjny: Windows
- Python: 3.14.3
- Biblioteka python-docx: 1.2.0
- LibreOffice – obsługa konwersji dokumentów do PDF
- Visual Studio Code
- Framework testowy: unittest

Testy wykonano również w nowym środowisku wirtualnym `.venv`, po instalacji zależności z pliku `requirements.txt`.

## 3. Testy automatyczne

Przygotowano 22 testy automatyczne.

| Obszar | Liczba testów | Wynik |
|---|---:|---|
| Konwersja CSV i JSON | 9 | Zaliczono |
| Konwersja TXT i DOCX | 3 | Zaliczono |
| Konwersja dokumentów do PDF | 6 | Zaliczono |
| Rejestr konwerterów i walidacja | 4 | Zaliczono |
| **Razem** | **22** | **22/22** |

Testy obejmowały poprawne i błędne dane, zachowanie polskich znaków, puste wartości, nieprawidłową liczbę kolumn CSV, błędny JSON, odrzucanie zagnieżdżonych danych JSON, brak plików, nieobsługiwane konwersje oraz zabezpieczenie przed nadpisaniem.

Sprawdzono również obsługę braku LibreOffice i błędu uruchomienia procesu zewnętrznego.

## 4. Testy manualne

| Przypadek | Oczekiwany rezultat | Wynik |
|---|---|---|
| Wybór pliku DOCX | Dostępne tylko TXT i PDF | Zaliczono |
| Konwersja DOCX → PDF przez GUI | Utworzenie PDF | Zaliczono |
| Powtórzenie konwersji | Propozycja bezpiecznej nazwy | Zaliczono |
| Uszkodzony JSON | Komunikat błędu bez zamknięcia aplikacji | Zaliczono |
| Aktualizacja statusu | Status zgodny z wyborem użytkownika | Zaliczono |
| Uruchomienie `main.py` | Otwarcie interfejsu graficznego | Zaliczono |

## 5. Wynik końcowy

Ostatnie pełne uruchomienie testów automatycznych:

```text
Ran 22 tests in 3.711s

OK
```

Wszystkie 22 testy automatyczne zakończyły się pomyślnie.

## 6. Wnioski

Aplikacja realizuje sześć wymaganych kierunków konwersji i obsługuje podstawowe sytuacje błędne.

Zastosowanie rejestru konwerterów pozwala oddzielić logikę konwersji od interfejsu graficznego. Operacje konwersji wykonywane są w osobnym wątku, a błędy są prezentowane użytkownikowi i zapisywane w dzienniku.

Przeprowadzone testy potwierdzają działanie zaimplementowanych funkcji w sprawdzonym środowisku. Nie gwarantują identycznego zachowania na wszystkich systemach operacyjnych ani zachowania złożonego formatowania dokumentów.

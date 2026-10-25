# Raport testów – Uniwersalny konwerter plików

**Przedmiot:** Programowanie V  
**Projekt:** Uniwersalny konwerter plików  
**Autor:** Tomasz Kroker

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

Przygotowano 20 testów automatycznych.

| Obszar | Liczba testów | Wynik |
|---|---:|---|
| Konwersja CSV i JSON | 8 | Zaliczono |
| Konwersja TXT i DOCX | 3 | Zaliczono |
| Konwersja dokumentów do PDF | 5 | Zaliczono |
| Rejestr konwerterów i walidacja | 4 | Zaliczono |
| **Razem** | **20** | **20/20** |

Testy obejmowały poprawne i błędne dane, zachowanie polskich znaków, puste wartości, nieprawidłową liczbę kolumn CSV, błędny JSON, brak plików, nieobsługiwane konwersje oraz zabezpieczenie przed nadpisaniem.

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
Ran 20 tests in 3.639s

OK
```

Wszystkie testy automatyczne zakończyły się pomyślnie.

## 6. Wnioski

Aplikacja realizuje sześć wymaganych kierunków konwersji i obsługuje podstawowe sytuacje błędne.

Zastosowanie rejestru konwerterów pozwala oddzielić logikę konwersji od interfejsu graficznego. Operacje konwersji wykonywane są w osobnym wątku, a błędy są prezentowane użytkownikowi i zapisywane w dzienniku.

Przeprowadzone testy potwierdzają działanie zaimplementowanych funkcji w sprawdzonym środowisku. Nie gwarantują identycznego zachowania na wszystkich systemach operacyjnych ani zachowania złożonego formatowania dokumentów.

# Uniwersalny konwerter plików

## 1. Opis projektu

Uniwersalny konwerter plików to aplikacja desktopowa umożliwiająca konwersję plików pomiędzy wybranymi formatami.

Program został wykonany w języku Python, z wykorzystaniem biblioteki Tkinter/ttk do stworzenia interfejsu graficznego.

Aplikacja umożliwia:

- Wybór pliku wejściowego.
- Automatyczne rozpoznawanie dostępnych formatów docelowych.
- Wybór katalogu zapisu.
- Konwersję plików za pomocą odpowiednich bibliotek i narzędzi.
- Bezpieczne zapisywanie plików bez nadpisywania istniejących danych.
- Wyświetlanie komunikatów o powodzeniu i błędach.
- Zapisywanie szczegółów błędów w dzienniku aplikacji.

## 2. Obsługiwane formaty

Aplikacja obsługuje sześć kierunków konwersji podzielonych na trzy grupy.

| Grupa | Konwersja | Narzędzie |
|---|---|---|
| Dane strukturalne | CSV → JSON | csv, json |
| Dane strukturalne | JSON → CSV | json, csv |
| Tekst i dokumenty | TXT → DOCX | python-docx |
| Tekst i dokumenty | DOCX → TXT | python-docx |
| Dokumenty biurowe | DOCX → PDF | LibreOffice |
| Dokumenty biurowe | ODT → PDF | LibreOffice |

Aplikacja pokazuje wyłącznie formaty dostępne dla wskazanego pliku wejściowego.

## 3. Wymagania

Do uruchomienia aplikacji potrzebne są:

- Python 3 z obsługą Tkinter (projekt testowany na Python 3.14.3).
- Biblioteka python-docx 1.2.0.
- LibreOffice do wykonywania konwersji DOCX → PDF i ODT → PDF.
- System operacyjny obsługujący wymagane biblioteki i narzędzia.

Projekt był rozwijany i testowany na systemie Windows.

Tkinter, csv, json, pathlib, subprocess, tempfile, threading, queue, logging i unittest należą do standardowej biblioteki Pythona.

LibreOffice jest zewnętrznym programem i wymaga osobnej instalacji.

## 4. Instalacja

### 4.1. Pobranie projektu

Repozytorium GitHub:

https://github.com/tomasz-kroker/Programowanie-V

Pobranie projektu za pomocą Git:

```bash
git clone https://github.com/tomasz-kroker/Programowanie-V.git
cd Programowanie-V
```

### 4.2. Utworzenie środowiska wirtualnego

W systemie Windows:

```powershell
python -m venv .venv
```

### 4.3. Instalacja zależności

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Polecenie instaluje bibliotekę python-docx oraz wymagane przez nią zależności.

### 4.4. Instalacja LibreOffice

Do konwersji dokumentów biurowych na PDF należy zainstalować LibreOffice:

https://www.libreoffice.org/

Aplikacja wyszukuje LibreOffice w zmiennej PATH oraz w typowych lokalizacjach instalacji.

W przypadku braku LibreOffice format PDF może nadal pojawiać się na liście dostępnych formatów docelowych. Jednak podczas próby konwersji DOCX → PDF lub ODT → PDF aplikacja wykryje brak programu i wyświetli odpowiedni komunikat błędu.

Aby korzystać z tych konwersji, należy zainstalować LibreOffice.

## 5. Uruchamianie aplikacji

W systemie Windows, z katalogu głównego projektu:

```powershell
.\.venv\Scripts\python.exe main.py
```

Jeśli wymagane biblioteki są zainstalowane w aktywnym środowisku Pythona, można również użyć:

```powershell
python main.py
```

Po uruchomieniu pojawi się okno aplikacji „Uniwersalny konwerter plików”.

Dostępny jest także plik `gui.py`, który można uruchomić bezpośrednio.

## 6. Instrukcja użytkowania

1. Uruchom aplikację.
2. Kliknij „Przeglądaj” przy polu pliku wejściowego.
3. Wybierz plik przeznaczony do konwersji.
4. Wybierz jeden z dostępnych formatów docelowych.
5. Wskaż katalog zapisu.
6. Kliknij „Konwertuj”.
7. Po zakończeniu operacji odczytaj komunikat z lokalizacją pliku wynikowego.

Jeżeli plik wynikowy już istnieje, aplikacja umożliwia zapisanie nowego pliku pod inną nazwą, np. `dokument_1.pdf`.

Podczas konwersji przyciski i pola wyboru są blokowane, a dłuższa operacja wykonywana jest w osobnym wątku, aby nie blokować interfejsu.

## 7. Zasady konwersji CSV i JSON

### CSV → JSON

- Separatorem kolumn jest przecinek.
- Pierwszy wiersz CSV określa nazwy kolumn.
- Dane odczytywane są w UTF-8, z obsługą znacznika BOM.
- Wartości z CSV zapisywane są jako tekst.
- Zachowywane są nazwy i kolejność kolumn oraz kolejność rekordów.
- Obsługiwane są polskie znaki i puste wartości.
- Nieprawidłowa liczba kolumn powoduje zgłoszenie błędu.

### JSON → CSV

Akceptowana struktura JSON to niepusta lista obiektów o jednakowym zestawie kluczy.

Przykład:

```json
[
    {
        "imie": "Jan",
        "miasto": "Opole"
    },
    {
        "imie": "Anna",
        "miasto": "Gogolin"
    }
]
```

Nazwy kolumn pochodzą z kluczy pierwszego obiektu. Ich kolejność jest zachowywana.

Konwersja JSON → CSV obsługuje płaskie obiekty zawierające wyłącznie wartości tekstowe. Wartości liczbowe, logiczne, null oraz zagnieżdżone obiekty i tablice są odrzucane z odpowiednim komunikatem błędu.

## 8. Ograniczenia projektu

- Program obsługuje tylko zadeklarowane kierunki konwersji.
- TXT nie przechowuje formatowania dokumentu.
- Konwersja DOCX → TXT odczytuje akapity dokumentu; nie przenosi złożonych elementów, takich jak tabele i wykresy.
- TXT → DOCX zachowuje tekst i podział na akapity, ale nie odtwarza zaawansowanego formatowania.
- Konwersja do PDF wykorzystuje LibreOffice, a wynik może różnić się układem od dokumentu źródłowego.
- Nie jest gwarantowane zachowanie makr, przypisów ani złożonych elementów dokumentów.
- Obsługa CSV i JSON jest przeznaczona przede wszystkim do prostych danych tabelarycznych.
- Aplikacja nie umożliwia konwersji wszystkich możliwych formatów plików.

## 9. Obsługa błędów

Aplikacja sprawdza między innymi:

- Istnienie pliku wejściowego.
- Poprawność wyboru formatu docelowego.
- Istnienie katalogu zapisu.
- Konflikt nazwy pliku wynikowego.
- Poprawność struktury plików CSV i JSON.
- Dostępność LibreOffice.
- Poprawność zakończenia zewnętrznego procesu konwersji.
- Istnienie wygenerowanego pliku PDF.

Błędy wyświetlane są w oknach komunikatów.

Dodatkowo szczegółowe informacje o błędach zapisywane są w pliku `conversion.log`, który nie jest umieszczany w repozytorium Git.

## 10. Testowanie

Projekt zawiera testy automatyczne wykonane z wykorzystaniem modułu `unittest`.

Uruchomienie wszystkich testów:

```powershell
python -m unittest discover -s tests -v
```

Lub w środowisku wirtualnym Windows:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Przeprowadzono 22 testy automatyczne, obejmujące między innymi:

- Konwersję CSV i JSON.
- Konwersję TXT i DOCX.
- Konwersję DOCX i ODT do PDF.
- Poprawność polskich znaków.
- Zachowanie pustych wartości.
- Nieprawidłową strukturę JSON.
- Niepoprawną liczbę kolumn CSV.
- Brak pliku wejściowego.
- Nieobsługiwany kierunek konwersji.
- Zabezpieczenie przed nadpisywaniem.
- Symulację braku LibreOffice.
- Obsługę dostępnych formatów w rejestrze konwerterów.

**Wynik ostatniego uruchomienia: 22 testy, wszystkie zakończone pomyślnie**

Projekt został również sprawdzony w nowym środowisku wirtualnym Python z zależnościami zainstalowanymi za pomocą `requirements.txt`.

Testy konwersji PDF wymagają dostępnego LibreOffice. Test ODT → PDF wykorzystuje przykładowy dokument `sample_files/przyklad.odt`.

## 11. Struktura projektu

```text
Programowanie-V/
├── converters/
│   ├── csv_json.py
│   ├── txt_docx.py
│   ├── office_pdf.py
│   └── registry.py
├── sample_files/
├── tests/
│   ├── test_csv_json.py
│   ├── test_txt_docx.py
│   ├── test_office_pdf.py
│   └── test_registry.py
├── main.py
├── gui.py
├── demo.py
├── requirements.txt
├── .gitignore
└── README.md
```

Katalog `sample_files` zawiera przykładowe pliki wejściowe, m.in. CSV, JSON, TXT i ODT, oraz pliki wykorzystywane podczas testowania.

Plik `demo.py` zawiera wcześniejszą demonstrację konwersji wykonywanych z poziomu terminala.

## 12. Historia realizacji

Projekt był rozwijany etapami:

- **Laboratorium 2:** konwersje CSV ↔ JSON, podstawowe testy i repozytorium Git.
- **Laboratorium 3:** konwersje TXT ↔ DOCX, DOCX → PDF i ODT → PDF oraz ich testowanie.
- **Laboratorium 4:** interfejs graficzny Tkinter/ttk, dynamiczny wybór formatów, obsługa konwersji i konfliktów nazw.
- **Laboratorium 5:** rozbudowa walidacji, obsługa błędów, automatyczne wyszukiwanie LibreOffice, testy i dokumentacja.

Historia postępu projektu dostępna jest w commitach repozytorium GitHub.

## 13. Wykorzystane źródła i narzędzia

- Python – https://docs.python.org/3/
- Tkinter – https://docs.python.org/3/library/tkinter.html
- python-docx – https://python-docx.readthedocs.io/
- LibreOffice – https://www.libreoffice.org/
- Dokumentacja modułu subprocess – https://docs.python.org/3/library/subprocess.html
- Instrukcja projektowa przedmiotu Programowanie V – „Projekt 1. Uniwersalny konwerter plików”.

W trakcie realizacji wykorzystano również **ChatGPT (OpenAI)** jako narzędzie wspomagające projektowanie aplikacji, przygotowanie fragmentów kodu, analizę błędów, opracowanie testów i dokumentacji.

Implementacja była uruchamiana i testowana etapami w środowisku Visual Studio Code.

## 14. Autor

**Tomasz Kroker**

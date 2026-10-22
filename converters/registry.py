from pathlib import Path
from converters.csv_json import csv_to_json, json_to_csv
from converters.txt_docx import txt_to_docx, docx_to_txt
from converters.office_pdf import docx_to_pdf, odt_to_pdf

CONVERTERS = {
    (".csv", ".json"): csv_to_json,
    (".json", ".csv"): json_to_csv,
    (".txt", ".docx"): txt_to_docx,
    (".docx", ".txt"): docx_to_txt,
    (".docx", ".pdf"): docx_to_pdf,
    (".odt", ".pdf"): odt_to_pdf,
}


def available_targets(source: Path) -> list[str]:

    source_format = source.suffix.lower()

    return sorted(
        target
        for (source_ext, target) in CONVERTERS
        if source_ext == source_format
    )


def execute(source: Path, destination: Path) -> Path:

    if not source.is_file():
        raise FileNotFoundError(
            "Nie znaleziono pliku wejściowego."
        )

    if not destination.parent.is_dir():
        raise NotADirectoryError(
            "Katalog docelowy nie istnieje."
        )

    source_format = source.suffix.lower()
    target_format = destination.suffix.lower()

    conversion = (source_format, target_format)

    if conversion not in CONVERTERS:
        raise ValueError(
            f"Nieobsługiwana konwersja: "
            f"{source_format} -> {target_format}"
        )

    if destination.exists():
        raise FileExistsError(
            "Plik docelowy już istnieje."
        )

    converter = CONVERTERS[conversion]

    return converter(source, destination)

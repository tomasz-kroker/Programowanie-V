import csv
import json
from pathlib import Path


def csv_to_json(source: Path, destination: Path) -> Path:

    with source.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Plik CSV nie zawiera nagłówków.")

        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("Plik CSV zawiera powtarzające się nagłówki.")

        data = list(reader)

        if any(None in row for row in data):
            raise ValueError("Nieprawidłowa liczba kolumn w pliku CSV.")

    with destination.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return destination


def json_to_csv(source: Path, destination: Path) -> Path:

    with source.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, list) or not data:
        raise ValueError("JSON musi zawierać niepustą listę obiektów.")

    if not all(isinstance(row, dict) for row in data):
        raise ValueError("Każdy element JSON musi być obiektem.")

    headers = list(data[0].keys())

    if not headers:
        raise ValueError("Obiekty JSON nie zawierają kolumn.")

    if any(set(row.keys()) != set(headers) for row in data):
        raise ValueError("Obiekty JSON mają różne kolumny.")

    with destination.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    return destination


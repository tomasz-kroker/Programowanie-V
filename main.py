from pathlib import Path
from converters.csv_json import csv_to_json, json_to_csv


def main():
    project_dir = Path(__file__).resolve().parent
    sample_dir = project_dir / "sample_files"

    source_csv = sample_dir / "osoby.csv"
    output_json = sample_dir / "osoby.json"
    output_csv = sample_dir / "osoby_powrot.csv"

    try:
        csv_to_json(source_csv, output_json)
        print("CSV -> JSON: zakończono pomyślnie!")

        json_to_csv(output_json, output_csv)
        print("JSON -> CSV: zakończono pomyślnie!")

        print("\nUtworzone pliki:")
        print(output_json)
        print(output_csv)

    except (OSError, ValueError) as error:
        print(f"Błąd konwersji: {error}")


if __name__ == "__main__":
    main()

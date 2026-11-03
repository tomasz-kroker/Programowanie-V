from pathlib import Path
from converters.csv_json import csv_to_json, json_to_csv
from converters.txt_docx import txt_to_docx, docx_to_txt
from converters.office_pdf import docx_to_pdf, odt_to_pdf


def main():
    project_dir = Path(__file__).resolve().parent
    sample_dir = project_dir / "sample_files"

    source_csv = sample_dir / "osoby.csv"
    output_json = sample_dir / "osoby.json"
    output_csv = sample_dir / "osoby_powrot.csv"

    source_txt = sample_dir / "przyklad.txt"
    output_docx = sample_dir / "przyklad.docx"
    output_txt = sample_dir / "przyklad_powrot.txt"

    output_pdf = sample_dir / "przyklad.pdf"
    source_odt = sample_dir / "przyklad.odt"
    output_odt_pdf = sample_dir / "przyklad_odt.pdf"

    try:
        csv_to_json(source_csv, output_json)
        print("CSV -> JSON: zakończono pomyślnie!")

        json_to_csv(output_json, output_csv)
        print("JSON -> CSV: zakończono pomyślnie!")

        txt_to_docx(source_txt, output_docx)
        print("TXT -> DOCX: zakończono pomyślnie!")

        docx_to_txt(output_docx, output_txt)
        print("DOCX -> TXT: zakończono pomyślnie!")

        docx_to_pdf(output_docx, output_pdf)
        print("DOCX -> PDF: zakończono pomyślnie!")

        odt_to_pdf(source_odt, output_odt_pdf)
        print("ODT -> PDF: zakończono pomyślnie!")

        print("\nUtworzone pliki:")
        print(output_json)
        print(output_csv)
        print(output_docx)
        print(output_txt)
        print(output_pdf)
        print(output_odt_pdf)

    except (OSError, ValueError, RuntimeError) as error:
        print(f"Błąd konwersji: {error}")


if __name__ == "__main__":
    main()

import subprocess
import shutil
import tempfile
from pathlib import Path
import os


def find_libreoffice() -> Path | None:

    for name in ("soffice", "libreoffice"):
        executable = shutil.which(name)

        if executable:
            return Path(executable)

    candidates = []

    for variable in ("ProgramFiles", "ProgramFiles(x86)"):
        base = os.environ.get(variable)

        if base:
            candidates.append(
                Path(base) / "LibreOffice" / "program" / "soffice.exe"
            )

    candidates.extend([
        Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
        Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
        Path("/usr/bin/libreoffice"),
        Path("/usr/bin/soffice"),
        Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"),
    ])

    for path in candidates:
        if path.is_file():
            return path

    return None



def office_to_pdf(source: Path, destination: Path) -> Path:

    libreoffice = find_libreoffice()

    if not source.is_file():
        raise FileNotFoundError("Nie znaleziono pliku wejściowego.")

    if source.suffix.lower() not in (".docx", ".odt"):
        raise ValueError("Obsługiwane są tylko pliki DOCX i ODT.")

    if libreoffice is None:
        raise FileNotFoundError(
        "Nie znaleziono LibreOffice. "
        "Zainstaluj LibreOffice i spróbuj ponownie."
    )

    if destination.suffix.lower() != ".pdf":
        raise ValueError("Plik wynikowy musi mieć rozszerzenie PDF.")

    if destination.exists():
        raise FileExistsError("Plik PDF już istnieje.")

    if not destination.parent.is_dir():
        raise NotADirectoryError("Katalog docelowy nie istnieje.")

    with tempfile.TemporaryDirectory() as folder:
        temp_dir = Path(folder)

        command = [
            str(libreoffice),
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(temp_dir),
            str(source.resolve())
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60
            )
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(
                "Przekroczono czas konwersji."
            ) from error

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
                or "LibreOffice nie wykonał konwersji."
            )

        generated_pdf = temp_dir / f"{source.stem}.pdf"

        if not generated_pdf.is_file():
            raise RuntimeError(
                "LibreOffice nie utworzył pliku PDF."
            )

        shutil.move(str(generated_pdf), str(destination))

    return destination


def docx_to_pdf(source: Path, destination: Path) -> Path:
    if source.suffix.lower() != ".docx":
        raise ValueError("Wymagany plik DOCX.")

    return office_to_pdf(source, destination)


def odt_to_pdf(source: Path, destination: Path) -> Path:
    if source.suffix.lower() != ".odt":
        raise ValueError("Wymagany plik ODT.")

    return office_to_pdf(source, destination)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from threading import Thread
from queue import Queue, Empty

from converters.registry import available_targets, execute


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Uniwersalny konwerter plików")
        self.root.geometry("650x420")
        self.root.resizable(False, False)

        self.source_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.target_format = tk.StringVar()
        self.status = tk.StringVar(value="Wybierz plik wejściowy.")

        self.busy = False
        self.results = Queue()

        frame = ttk.Frame(root, padding=25)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Uniwersalny konwerter plików",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(0, 20))

        ttk.Label(
            frame,
            text="Plik wejściowy:"
        ).pack(anchor="w")

        file_frame = ttk.Frame(frame)
        file_frame.pack(fill="x", pady=(5, 15))

        ttk.Entry(
            file_frame,
            textvariable=self.source_file,
            state="readonly"
        ).pack(side="left", fill="x", expand=True)

        self.file_button = ttk.Button(
            file_frame,
            text="Przeglądaj",
            command=self.select_file
        )
        self.file_button.pack(side="left", padx=(10, 0))

        ttk.Label(
            frame,
            text="Format docelowy:"
        ).pack(anchor="w")

        self.format_combo = ttk.Combobox(
            frame,
            textvariable=self.target_format,
            state="readonly"
        )
        self.format_combo.pack(fill="x", pady=(5, 15))

        self.format_combo.bind(
            "<<ComboboxSelected>>",
            self.update_status
        )

        ttk.Label(
            frame,
            text="Katalog zapisu:"
        ).pack(anchor="w")

        folder_frame = ttk.Frame(frame)
        folder_frame.pack(fill="x", pady=(5, 20))

        ttk.Entry(
            folder_frame,
            textvariable=self.output_dir,
            state="readonly"
        ).pack(side="left", fill="x", expand=True)

        self.folder_button = ttk.Button(
            folder_frame,
            text="Przeglądaj",
            command=self.select_folder
        )
        self.folder_button.pack(side="left", padx=(10, 0))

        self.convert_button = ttk.Button(
            frame,
            text="Konwertuj",
            command=self.convert,
            state="disabled"
        )
        self.convert_button.pack(fill="x", pady=10)

        ttk.Label(
            frame,
            textvariable=self.status
        ).pack(pady=10)

        for variable in (
            self.source_file,
            self.output_dir,
            self.target_format
        ):
            variable.trace_add("write", self.update_button)

    def update_button(self, *args):

        source = Path(self.source_file.get())

        ready = (
            not self.busy
            and source.is_file()
            and bool(self.output_dir.get())
            and Path(self.output_dir.get()).is_dir()
            and self.target_format.get()
            in available_targets(source)
        )

        self.convert_button.config(
            state="normal" if ready else "disabled"
        )

    def update_status(self, event=None):

        if self.busy:
            return

        source = Path(self.source_file.get())

        if not self.source_file.get():
            self.status.set("Wybierz plik wejściowy.")

        elif not source.is_file():
            self.status.set("Nie znaleziono pliku wejściowego.")

        elif not available_targets(source):
            self.status.set("Brak dostępnych konwersji.")

        elif self.target_format.get() not in available_targets(source):
            self.status.set("Wybierz format docelowy.")

        elif not self.output_dir.get():
            self.status.set("Wybierz katalog zapisu.")

        elif not Path(self.output_dir.get()).is_dir():
            self.status.set("Nie znaleziono katalogu zapisu.")

        else:
            self.status.set("Gotowy do konwersji.")

        self.update_button()

    def select_file(self):

        if self.busy:
            return

        filename = filedialog.askopenfilename(
            title="Wybierz plik",
            filetypes=[
                (
                    "Obsługiwane pliki",
                    "*.csv *.json *.txt *.docx *.odt"
                ),
                ("Wszystkie pliki", "*.*")
            ]
        )

        if filename:
            self.source_file.set(filename)

            targets = available_targets(Path(filename))

            self.format_combo["values"] = targets
            self.target_format.set("")

            self.update_status()

    def select_folder(self):

        if self.busy:
            return

        folder = filedialog.askdirectory(
            title="Wybierz katalog zapisu"
        )

        if folder:
            self.output_dir.set(folder)
            self.update_status()

    def convert(self):

        if self.busy:
            return

        source = Path(self.source_file.get())
        output_dir = Path(self.output_dir.get())
        target = self.target_format.get()

        if not source.is_file():
            messagebox.showerror(
                "Błąd", "Nie znaleziono pliku wejściowego."
            )
            return

        if not output_dir.is_dir():
            messagebox.showerror(
                "Błąd", "Nie znaleziono katalogu zapisu."
            )
            return

        if target not in available_targets(source):
            messagebox.showerror(
                "Błąd", "Nieobsługiwany format docelowy."
            )
            return

        destination = output_dir / f"{source.stem}{target}"

        if destination.exists():
            answer = messagebox.askyesno(
                "Plik już istnieje",
                "Plik wynikowy już istnieje.\n"
                "Czy zapisać wynik pod inną nazwą?"
            )

            if not answer:
                self.status.set("Anulowano konwersję.")
                return

            number = 1

            while destination.exists():
                destination = (
                    output_dir /
                    f"{source.stem}_{number}{target}"
                )
                number += 1

        self.busy = True
        self.convert_button.config(state="disabled")
        self.file_button.config(state="disabled")
        self.folder_button.config(state="disabled")
        self.format_combo.config(state="disabled")

        self.status.set("Trwa konwersja...")

        worker = Thread(
            target=self.run_conversion,
            args=(source, destination),
            daemon=True
        )

        worker.start()

        self.root.after(100, self.check_result)

    def run_conversion(self, source, destination):

        try:
            result = execute(source, destination)
            self.results.put(("success", result))

        except Exception as error:
            self.results.put(("error", str(error)))

    def check_result(self):

        try:
            result_type, value = self.results.get_nowait()

        except Empty:
            self.root.after(100, self.check_result)
            return

        self.busy = False

        self.file_button.config(state="normal")
        self.folder_button.config(state="normal")
        self.format_combo.config(state="readonly")

        self.update_button()

        if result_type == "success":
            self.status.set("Konwersja zakończona pomyślnie!")

            messagebox.showinfo(
                "Sukces",
                f"Utworzono plik:\n{value}"
            )

        else:
            self.status.set("Błąd konwersji.")

            messagebox.showerror(
                "Błąd konwersji",
                value
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
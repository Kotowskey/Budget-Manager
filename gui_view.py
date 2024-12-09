# gui_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from typing import Optional, Tuple, Dict

class BudzetGUIView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Budget Manager")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create a container for frames
        self.container = ttk.Frame(self.root)
        self.container.pack(fill='both', expand=True)

        self.frames = {}

        for F in (WelcomeFrame, LoginFrame, MainMenuFrame, TransactionsFrame, SummaryFrame, LimitsFrame, ImportExportFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomeFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def run(self):
        self.root.mainloop()

    def wyswietl_welcome_screen(self):
        self.show_frame(WelcomeFrame)

    def wyswietl_glowne_menu_kategorii(self):
        self.show_frame(MainMenuFrame)

    def wyswietl_ekran_logowania(self):
        self.show_frame(LoginFrame)

    def wyswietl_podmenu_transakcje(self):
        self.show_frame(TransactionsFrame)

    def wyswietl_podmenu_podsumowania(self):
        self.show_frame(SummaryFrame)

    def wyswietl_podmenu_limity(self):
        self.show_frame(LimitsFrame)

    def wyswietl_podmenu_import_eksport(self):
        self.show_frame(ImportExportFrame)

    def wyswietl_transakcje(self, transakcje: list):
        self.frames[TransactionsFrame].update_transakcje(transakcje)

    def wyswietl_podsumowanie(self, saldo: float):
        self.frames[SummaryFrame].update_saldo(saldo)

    def wyswietl_limity(self, limity: Dict[str, float]):
        self.frames[LimitsFrame].update_limity(limity)

    def wyswietl_raport_wydatkow(self, raport: Dict[str, float]):
        ReportWindow(self.root, "Raport Wydatków", raport)

    def wyswietl_raport_przychodow(self, raport: Dict[str, float]):
        ReportWindow(self.root, "Raport Przychodów", raport)

    def wyswietl_wykres_wydatkow(self, raport: Dict[str, float]):
        ReportWindow(self.root, "Wykres Wydatków", raport, wykres=True)

    def wyswietl_wykres_przychodow(self, raport: Dict[str, float]):
        ReportWindow(self.root, "Wykres Przychodów", raport, wykres=True)

    def wyswietl_komunikat(self, komunikat: str):
        messagebox.showinfo("Informacja", komunikat)

    def pobierz_potwierdzenie(self, komunikat: str) -> bool:
        return messagebox.askyesno("Potwierdzenie", komunikat)

    def wyswietl_wyjscie(self):
        self.show_frame(WelcomeFrame)
        self.on_close()

    def zakoncz(self):
        self.on_close()

    def on_close(self):
        self.controller.model.zapisz_dane()  # Zakładając, że model ma metodę zapisującą dane
        self.root.destroy()

class WelcomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Witamy w Budget Manager!", font=("Helvetica", 24))
        label.pack(pady=20)

        start_button = ttk.Button(self, text="Rozpocznij", command=self.start)
        start_button.pack(pady=10)

        exit_button = ttk.Button(self, text="Wyjście", command=self.controller.on_close)
        exit_button.pack(pady=10)

    def start(self):
        self.controller.wyswietl_ekran_logowania()

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Logowanie/Rejestracja", font=("Helvetica", 18))
        label.pack(pady=20)

        login_button = ttk.Button(self, text="Logowanie", command=self.login)
        login_button.pack(pady=10)

        register_button = ttk.Button(self, text="Rejestracja", command=self.register)
        register_button.pack(pady=10)

        exit_button = ttk.Button(self, text="Wyjście", command=self.controller.on_close)
        exit_button.pack(pady=10)

    def login(self):
        login = simpledialog.askstring("Login", "Podaj login:", parent=self)
        if login is None:
            return
        haslo = simpledialog.askstring("Hasło", "Podaj hasło:", show='*', parent=self)
        if haslo is None:
            return
        success = self.controller.controller.model.zaloguj(login, haslo)
        if success:
            self.controller.controller.zalogowany_uzytkownik = login
            self.controller.wyswietl_komunikat(f"Zalogowano jako {login}.")
            self.controller.wyswietl_glowne_menu_kategorii()
        else:
            self.controller.wyswietl_komunikat("Nieprawidłowy login lub hasło.")

    def register(self):
        login = simpledialog.askstring("Rejestracja", "Podaj nowy login:", parent=self)
        if login is None:
            return
        haslo = simpledialog.askstring("Rejestracja", "Podaj nowe hasło:", show='*', parent=self)
        if haslo is None:
            return
        success = self.controller.controller.model.zarejestruj(login, haslo)
        if success:
            self.controller.wyswietl_komunikat("Rejestracja udana. Możesz się teraz zalogować.")
        else:
            self.controller.wyswietl_komunikat("Użytkownik o takim loginie już istnieje.")

class MainMenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Główne Menu", font=("Helvetica", 18))
        label.pack(pady=20)

        transakcje_button = ttk.Button(self, text="Transakcje", command=self.transakcje)
        transakcje_button.pack(pady=10)

        podsumowania_button = ttk.Button(self, text="Podsumowania", command=self.podsumowania)
        podsumowania_button.pack(pady=10)

        limity_button = ttk.Button(self, text="Limity", command=self.limity)
        limity_button.pack(pady=10)

        import_export_button = ttk.Button(self, text="Importowanie i eksportowanie", command=self.import_export)
        import_export_button.pack(pady=10)

        wyjscie_button = ttk.Button(self, text="Wyjście", command=self.controller.on_close)
        wyjscie_button.pack(pady=10)

    def transakcje(self):
        self.controller.wyswietl_podmenu_transakcje()

    def podsumowania(self):
        self.controller.wyswietl_podmenu_podsumowania()

    def limity(self):
        self.controller.wyswietl_podmenu_limity()

    def import_export(self):
        self.controller.wyswietl_podmenu_import_eksport()

class TransactionsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Transakcje", font=("Helvetica", 18))
        label.pack(pady=10)

        add_button = ttk.Button(self, text="Dodaj transakcję", command=self.dodaj_transakcje)
        add_button.pack(pady=5)

        edit_button = ttk.Button(self, text="Edytuj transakcję", command=self.edytuj_transakcje)
        edit_button.pack(pady=5)

        delete_button = ttk.Button(self, text="Usuń transakcję", command=self.usun_transakcje)
        delete_button.pack(pady=5)

        view_button = ttk.Button(self, text="Wyświetl transakcje", command=self.wyswietl_transakcje)
        view_button.pack(pady=5)

        back_button = ttk.Button(self, text="Powrót do głównego menu", command=self.controller.wyswietl_glowne_menu_kategorii)
        back_button.pack(pady=5)

        self.tree = ttk.Treeview(self, columns=("Nr", "Data", "Typ", "Kwota", "Kategoria", "Opis"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill='both', expand=True, pady=10)

    def dodaj_transakcje(self):
        dialog = TransakcjaDialog(self, "Dodaj Transakcję")
        self.wait_window(dialog.top)
        if dialog.result:
            # Przekazujemy dane do kontrolera
            self.controller.controller.dodaj_transakcje(dialog.result)
            self.wyswietl_transakcje()

    def edytuj_transakcje(self):
        selected = self.tree.selection()
        if not selected:
            self.controller.wyswietl_komunikat("Wybierz transakcję do edycji.")
            return
        indeks = int(self.tree.item(selected[0])['values'][0])
        transakcja = self.controller.controller.model.transakcje[indeks]
        dialog = TransakcjaDialog(self, "Edytuj Transakcję", edit=True, transakcja=transakcja)
        self.wait_window(dialog.top)
        if dialog.result:
            # Przekazujemy dane do kontrolera
            self.controller.controller.edytuj_transakcje(indeks, dialog.result)
            self.wyswietl_transakcje()

    def usun_transakcje(self):
        selected = self.tree.selection()
        if not selected:
            self.controller.wyswietl_komunikat("Wybierz transakcję do usunięcia.")
            return
        indeks = int(self.tree.item(selected[0])['values'][0])
        confirm = self.controller.pobierz_potwierdzenie("Czy na pewno chcesz usunąć wybraną transakcję?")
        if confirm:
            self.controller.controller.usun_transakcje(indeks)
            self.wyswietl_transakcje()

    def wyswietl_transakcje(self):
        transakcje = self.controller.controller.model.transakcje
        self.update_transakcje(transakcje)

    def update_transakcje(self, transakcje: list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, t in enumerate(transakcje):
            self.tree.insert("", "end", values=(idx, t.data, t.typ.capitalize(), f"{t.kwota:.2f}", t.kategoria, t.opis))

class SummaryFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Podsumowanie", font=("Helvetica", 18))
        label.pack(pady=10)

        self.saldo_label = ttk.Label(self, text="Aktualne saldo: 0.00 zł", font=("Helvetica", 14))
        self.saldo_label.pack(pady=10)

        raport_wydatkow_button = ttk.Button(self, text="Generuj raport wydatków", command=self.generuj_raport_wydatkow)
        raport_wydatkow_button.pack(pady=5)

        raport_przychodow_button = ttk.Button(self, text="Generuj raport przychodów", command=self.generuj_raport_przychodow)
        raport_przychodow_button.pack(pady=5)

        wykres_wydatkow_button = ttk.Button(self, text="Wyświetl wykres wydatków", command=self.wyswietl_wykres_wydatkow)
        wykres_wydatkow_button.pack(pady=5)

        wykres_przychodow_button = ttk.Button(self, text="Wyświetl wykres przychodów", command=self.wyswietl_wykres_przychodow)
        wykres_przychodow_button.pack(pady=5)

        back_button = ttk.Button(self, text="Powrót do głównego menu", command=self.controller.wyswietl_glowne_menu_kategorii)
        back_button.pack(pady=5)

    def update_saldo(self, saldo: float):
        self.saldo_label.config(text=f"Aktualne saldo: {saldo:.2f} zł")

    def generuj_raport_wydatkow(self):
        self.controller.controller.generuj_raport_wydatkow()

    def generuj_raport_przychodow(self):
        self.controller.controller.generuj_raport_przychodow()

    def wyswietl_wykres_wydatkow(self):
        self.controller.controller.wyswietl_wykres_wydatkow()

    def wyswietl_wykres_przychodow(self):
        self.controller.controller.wyswietl_wykres_przychodow()

class LimitsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Limity Budżetowe", font=("Helvetica", 18))
        label.pack(pady=10)

        ustaw_limit_button = ttk.Button(self, text="Ustaw limit", command=self.ustaw_limit)
        ustaw_limit_button.pack(pady=5)

        wyswietl_limity_button = ttk.Button(self, text="Wyświetl limity", command=self.wyswietl_limity)
        wyswietl_limity_button.pack(pady=5)

        usun_limit_button = ttk.Button(self, text="Usuń limit", command=self.usun_limit)
        usun_limit_button.pack(pady=5)

        back_button = ttk.Button(self, text="Powrót do głównego menu", command=self.controller.wyswietl_glowne_menu_kategorii)
        back_button.pack(pady=5)

    def ustaw_limit(self):
        dialog = LimitDialog(self, "Ustaw Limit")
        self.wait_window(dialog.top)
        if dialog.result:
            kategoria, limit = dialog.result
            self.controller.controller.ustaw_limit_budzetowy(kategoria, limit)

    def wyswietl_limity(self):
        limity = self.controller.controller.model.limity
        self.controller.wyswietl_limity(limity)

    def usun_limit(self):
        kategoria = simpledialog.askstring("Usuń Limit", "Podaj kategorię do usunięcia limitu:", parent=self)
        if kategoria:
            self.controller.controller.usun_limit(kategoria)
            # Aktualizacja widoku limity
            self.wyswietl_limity()

    def update_limity(self, limity: Dict[str, float]):
        message = "Aktualne limity:\n"
        if not limity:
            message += "Brak ustawionych limitów."
        else:
            for kategoria, limit in limity.items():
                message += f"{kategoria}: {limit:.2f} zł\n"
        self.controller.wyswietl_komunikat(message)

class ImportExportFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Importowanie i Eksportowanie", font=("Helvetica", 18))
        label.pack(pady=10)

        eksport_button = ttk.Button(self, text="Eksportuj transakcje do CSV", command=self.eksportuj)
        eksport_button.pack(pady=5)

        import_button = ttk.Button(self, text="Importuj transakcje z CSV", command=self.importuj)
        import_button.pack(pady=5)

        back_button = ttk.Button(self, text="Powrót do głównego menu", command=self.controller.wyswietl_glowne_menu_kategorii)
        back_button.pack(pady=5)

    def eksportuj(self):
        self.controller.controller.eksportuj_transakcje()

    def importuj(self):
        self.controller.controller.importuj_transakcje()

class ReportWindow(tk.Toplevel):
    def __init__(self, parent, title, raport, wykres=False):
        super().__init__(parent)
        self.title(title)
        self.geometry("600x400")
        label = ttk.Label(self, text=title, font=("Helvetica", 16))
        label.pack(pady=10)

        if wykres:
            self.display_chart(raport)
        else:
            text = tk.Text(self, wrap='word')
            text.pack(fill='both', expand=True, padx=10, pady=10)
            if not raport:
                text.insert('end', "Brak danych do wyświetlenia.")
            else:
                for kategoria, suma in raport.items():
                    text.insert('end', f"{kategoria}: {suma:.2f} zł\n")
            text.config(state='disabled')

        close_button = ttk.Button(self, text="Zamknij", command=self.destroy)
        close_button.pack(pady=10)

    def display_chart(self, raport):
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        if not raport:
            label = ttk.Label(self, text="Brak danych do wyświetlenia.")
            label.pack(pady=20)
            return

        categories = list(raport.keys())
        values = list(raport.values())

        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(categories, values, color='skyblue')
        ax.set_ylabel('Kwota (zł)')
        ax.set_title('Wykres')

        plt.xticks(rotation=45, ha='right')

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

class TransakcjaDialog:
    def __init__(self, parent, title, edit=False, transakcja=None):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.grab_set()

        ttk.Label(self.top, text="Typ:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.typ_var = tk.StringVar()
        self.typ_combobox = ttk.Combobox(self.top, textvariable=self.typ_var, values=["przychód", "wydatek"], state='readonly')
        self.typ_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.typ_combobox.current(0)

        ttk.Label(self.top, text="Kwota:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.kwota_entry = ttk.Entry(self.top)
        self.kwota_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.top, text="Kategoria:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.kategoria_entry = ttk.Entry(self.top)
        self.kategoria_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.top, text="Opis:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.opis_entry = ttk.Entry(self.top)
        self.opis_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.top, text="Data (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.data_entry = ttk.Entry(self.top)
        self.data_entry.grid(row=4, column=1, padx=10, pady=5)
        self.data_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        if edit and transakcja:
            self.typ_combobox.set(transakcja.typ)
            self.typ_combobox.config(state='disabled')
            self.kwota_entry.insert(0, str(transakcja.kwota))
            self.kategoria_entry.insert(0, transakcja.kategoria)
            self.opis_entry.insert(0, transakcja.opis)
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, transakcja.data)

        ttk.Button(self.top, text="OK", command=self.ok).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self.top, text="Anuluj", command=self.top.destroy).grid(row=5, column=1, padx=10, pady=10)

    def ok(self):
        typ = self.typ_var.get()
        try:
            kwota = float(self.kwota_entry.get())
            if kwota <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Błąd", "Kwota musi być liczbą większą od zera.")
            return
        kategoria = self.kategoria_entry.get().strip()
        if not kategoria:
            messagebox.showerror("Błąd", "Kategoria nie może być pusta.")
            return
        opis = self.opis_entry.get().strip()
        data = self.data_entry.get().strip()
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty.")
            return
        self.result = {
            'typ': typ,
            'kwota': kwota,
            'kategoria': kategoria,
            'opis': opis,
            'data': data
        }
        self.top.destroy()

class LimitDialog:
    def __init__(self, parent, title):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.grab_set()

        ttk.Label(self.top, text="Kategoria:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.kategoria_entry = ttk.Entry(self.top)
        self.kategoria_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.top, text="Limit (zł):").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.limit_entry = ttk.Entry(self.top)
        self.limit_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self.top, text="OK", command=self.ok).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(self.top, text="Anuluj", command=self.top.destroy).grid(row=2, column=1, padx=10, pady=10)

    def ok(self):
        kategoria = self.kategoria_entry.get().strip()
        if not kategoria:
            messagebox.showerror("Błąd", "Kategoria nie może być pusta.")
            return
        try:
            limit = float(self.limit_entry.get())
            if limit <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Błąd", "Limit musi być liczbą większą od zera.")
            return
        self.result = (kategoria, limit)
        self.top.destroy()

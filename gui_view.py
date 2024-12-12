import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import Transakcja

class BudzetGUIView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Aplikacja Budżetowa")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')  # Możesz wypróbować inne motywy, np. 'vista', 'alt', 'default'

        self.create_main_menu()
        self.create_frames()
        # self.create_notebook()  # Usunięto metodę tworzenia notebooka

    def run(self):
        self.root.mainloop()

    def create_main_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Plik Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Plik", menu=file_menu)
        file_menu.add_command(label="Wyloguj", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Wyjście", command=self.root.quit)

        # Transakcje Menu
        transactions_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Transakcje", menu=transactions_menu)
        transactions_menu.add_command(label="Dodaj transakcję", command=self.show_add_transaction)
        transactions_menu.add_command(label="Pokaż transakcje", command=self.show_transactions)

        # Podsumowania Menu
        summary_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Podsumowania", menu=summary_menu)
        summary_menu.add_command(label="Raport wydatków", command=self.show_expense_report)
        summary_menu.add_command(label="Raport przychodów", command=self.show_income_report)
        summary_menu.add_command(label="Wykres wydatków", command=self.show_expense_chart)
        summary_menu.add_command(label="Wykres przychodów", command=self.show_income_chart)

        # Limity Menu
        limits_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Limity", menu=limits_menu)
        limits_menu.add_command(label="Ustaw limit", command=self.set_limit)
        limits_menu.add_command(label="Pokaż limity", command=self.show_limits)

        # Import/Eksport Menu
        import_export_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Import/Eksport", menu=import_export_menu)
        import_export_menu.add_command(label="Eksportuj do CSV", command=self.export_to_csv)
        import_export_menu.add_command(label="Importuj z CSV", command=self.import_from_csv)

    def create_frames(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.welcome_label = ttk.Label(self.main_frame, text="Witaj w aplikacji budżetowej!", font=("Helvetica", 18, "bold"))
        self.welcome_label.pack(pady=30)

        self.login_button = ttk.Button(self.main_frame, text="Zaloguj się", command=self.show_login, width=20)
        self.login_button.pack(pady=10)

        self.register_button = ttk.Button(self.main_frame, text="Zarejestruj się", command=self.show_register, width=20)
        self.register_button.pack(pady=10)

    def show_login(self):
        login = simpledialog.askstring("Logowanie", "Podaj login:")
        if login:
            password = simpledialog.askstring("Logowanie", "Podaj hasło:", show='*')
            if password:
                if self.controller.model.zaloguj(login, password):
                    messagebox.showinfo("Logowanie", f"Zalogowano jako {login}")
                    self.update_main_frame_after_login()
                else:
                    messagebox.showerror("Błąd logowania", "Nieprawidłowy login lub hasło")

    def show_register(self):
        login = simpledialog.askstring("Rejestracja", "Podaj nowy login:")
        if login:
            password = simpledialog.askstring("Rejestracja", "Podaj hasło:", show='*')
            if password:
                if self.controller.model.zarejestruj(login, password):
                    messagebox.showinfo("Rejestracja", "Rejestracja udana. Możesz się teraz zalogować.")
                else:
                    messagebox.showerror("Błąd rejestracji", "Użytkownik o takim loginie już istnieje")

    def update_main_frame_after_login(self):
        # Ukryj główną ramkę logowania/rejestracji
        self.main_frame.pack_forget()

        # Stwórz nową ramkę dla po zalogowaniu
        self.logged_in_frame = ttk.Frame(self.root, padding="20")
        self.logged_in_frame.pack(fill=tk.BOTH, expand=True)

        # Powitanie użytkownika
        welcome_label = ttk.Label(self.logged_in_frame, text=f"Witaj, {self.controller.model.zalogowany_uzytkownik}!", font=("Helvetica", 16))
        welcome_label.pack(pady=20)

        # Wyświetlenie salda
        balance = self.controller.model.oblicz_saldo()
        balance_label = ttk.Label(self.logged_in_frame, text=f"Saldo: {balance:.2f} zł", font=("Helvetica", 14))
        balance_label.pack(pady=10)

        # Dodaj przyciski funkcji
        self.add_logged_in_buttons()

    def add_logged_in_buttons(self):
        # Ramka na przyciski
        buttons_frame = ttk.Frame(self.logged_in_frame, padding="10")
        buttons_frame.pack(pady=20)

        # Dodaj Transakcję
        add_transaction_button = ttk.Button(buttons_frame, text="Dodaj Transakcję", command=self.show_add_transaction, width=25)
        add_transaction_button.grid(row=0, column=0, padx=10, pady=10)

        # Pokaż Transakcje
        view_transactions_button = ttk.Button(buttons_frame, text="Pokaż Transakcje", command=self.show_transactions, width=25)
        view_transactions_button.grid(row=0, column=1, padx=10, pady=10)

        # Raport Wydatków
        expense_report_button = ttk.Button(buttons_frame, text="Raport Wydatków", command=self.show_expense_report, width=25)
        expense_report_button.grid(row=1, column=0, padx=10, pady=10)

        # Raport Przychodów
        income_report_button = ttk.Button(buttons_frame, text="Raport Przychodów", command=self.show_income_report, width=25)
        income_report_button.grid(row=1, column=1, padx=10, pady=10)

        # Wykres Wydatków
        expense_chart_button = ttk.Button(buttons_frame, text="Wykres Wydatków", command=self.show_expense_chart, width=25)
        expense_chart_button.grid(row=2, column=0, padx=10, pady=10)

        # Wykres Przychodów
        income_chart_button = ttk.Button(buttons_frame, text="Wykres Przychodów", command=self.show_income_chart, width=25)
        income_chart_button.grid(row=2, column=1, padx=10, pady=10)

        # Ustaw Limity
        set_limit_button = ttk.Button(buttons_frame, text="Ustaw Limity", command=self.set_limit, width=25)
        set_limit_button.grid(row=3, column=0, padx=10, pady=10)

        # Pokaż Limity
        show_limits_button = ttk.Button(buttons_frame, text="Pokaż Limity", command=self.show_limits, width=25)
        show_limits_button.grid(row=3, column=1, padx=10, pady=10)

    def logout(self):
        self.controller.model.zalogowany_uzytkownik = None
        messagebox.showinfo("Wylogowanie", "Wylogowano pomyślnie")
        self.logged_in_frame.pack_forget()
        self.create_frames()

    def show_add_transaction(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Dodaj transakcję")
        add_window.geometry("400x350")
        add_window.resizable(False, False)

        # Stylizacja
        add_window.configure(bg="#f0f0f0")

        # Ramka główna
        frame = ttk.Frame(add_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Kwota
        ttk.Label(frame, text="Kwota:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        amount_entry = ttk.Entry(frame)
        amount_entry.grid(row=0, column=1, pady=5, sticky=tk.EW)

        # Kategoria
        ttk.Label(frame, text="Kategoria:", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        category_entry = ttk.Entry(frame)
        category_entry.grid(row=1, column=1, pady=5, sticky=tk.EW)

        # Typ
        ttk.Label(frame, text="Typ:", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar(value="wydatek")
        type_combobox = ttk.Combobox(frame, textvariable=type_var, values=["wydatek", "przychód"], state="readonly")
        type_combobox.grid(row=2, column=1, pady=5, sticky=tk.EW)

        # Opis
        ttk.Label(frame, text="Opis:", font=("Helvetica", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        description_entry = ttk.Entry(frame)
        description_entry.grid(row=3, column=1, pady=5, sticky=tk.EW)

        # Konfiguracja kolumn
        frame.columnconfigure(1, weight=1)

        def add_transaction():
            try:
                amount = float(amount_entry.get())
                category = category_entry.get()
                transaction_type = type_var.get()
                description = description_entry.get()

                if not category:
                    raise ValueError("Kategoria nie może być pusta")

                transaction = Transakcja(
                    kwota=amount,
                    kategoria=category,
                    typ=transaction_type,
                    opis=description,
                    data=datetime.now().strftime('%Y-%m-%d')
                )

                self.controller.model.dodaj_transakcje(transaction)
                messagebox.showinfo("Sukces", "Transakcja dodana pomyślnie")
                add_window.destroy()
                self.update_main_frame_after_login()
            except ValueError as ve:
                messagebox.showerror("Błąd", f"Nieprawidłowa wartość: {ve}")

        # Przycisk Dodaj
        add_button = ttk.Button(frame, text="Dodaj", command=add_transaction)
        add_button.grid(row=4, column=0, columnspan=2, pady=20)

    def show_transactions(self):
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Lista transakcji")
        transactions_window.geometry("700x500")
        transactions_window.resizable(True, True)

        # Stylizacja
        transactions_window.configure(bg="#f0f0f0")

        # Ramka główna
        frame = ttk.Frame(transactions_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        columns = ("Kwota", "Kategoria", "Typ", "Opis", "Data")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        # Dodanie przewijania
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

        # Wstawienie danych
        for transaction in self.controller.model.transakcje:
            tree.insert("", "end", values=(transaction.kwota, transaction.kategoria, transaction.typ, transaction.opis, transaction.data))

    def show_expense_report(self):
        report = self.controller.model.generuj_raport_wydatkow()
        self.show_report("Raport wydatków", report)

    def show_income_report(self):
        report = self.controller.model.generuj_raport_przychodow()
        self.show_report("Raport przychodów", report)

    def show_report(self, title, report):
        if not report:
            messagebox.showinfo(title, "Brak danych do wyświetlenia raportu.")
            return

        report_window = tk.Toplevel(self.root)
        report_window.title(title)
        report_window.geometry("500x400")
        report_window.resizable(True, True)

        # Stylizacja
        report_window.configure(bg="#f0f0f0")

        # Ramka główna
        frame = ttk.Frame(report_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        columns = ("Kategoria", "Kwota")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        # Dodanie przewijania
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

        # Wstawienie danych
        for category, amount in report.items():
            tree.insert("", "end", values=(category, f"{amount:.2f} zł"))

    def show_expense_chart(self):
        report = self.controller.model.generuj_raport_wydatkow()
        self.show_chart("Wykres wydatków", report)

    def show_income_chart(self):
        report = self.controller.model.generuj_raport_przychodow()
        self.show_chart("Wykres przychodów", report)

    def show_chart(self, title, data):
        if not data:
            messagebox.showinfo("Brak danych", "Brak danych do wyświetlenia wykresu.")
            return

        chart_window = tk.Toplevel(self.root)
        chart_window.title(title)
        chart_window.geometry("600x500")
        chart_window.resizable(True, True)

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title(title)

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def set_limit(self):
        category = simpledialog.askstring("Ustaw limit", "Podaj kategorię:")
        if category:
            limit = simpledialog.askfloat("Ustaw limit", f"Podaj limit dla kategorii '{category}':", minvalue=0)
            if limit is not None:
                self.controller.model.ustaw_limit(category, limit)
                messagebox.showinfo("Sukces", f"Ustawiono limit {limit:.2f} zł dla kategorii '{category}'")

    def show_limits(self):
        limits = self.controller.model.limity
        if not limits:
            messagebox.showinfo("Limity", "Nie ustawiono żadnych limitów.")
            return
        self.show_report("Limity budżetowe", limits)

    def export_to_csv(self):
        try:
            self.controller.model.eksportuj_do_csv()
            messagebox.showinfo("Eksport", "Dane zostały wyeksportowane do pliku CSV")
        except Exception as e:
            messagebox.showerror("Eksport", f"Nie udało się wyeksportować danych: {e}")

    def import_from_csv(self):
        try:
            if self.controller.model.importuj_z_csv():
                messagebox.showinfo("Import", "Dane zostały zaimportowane z pliku CSV")
                self.update_main_frame_after_login()
            else:
                messagebox.showerror("Import", "Nie udało się zaimportować danych z pliku CSV")
        except Exception as e:
            messagebox.showerror("Import", f"Nie udało się zaimportować danych: {e}")

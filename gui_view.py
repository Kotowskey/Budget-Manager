import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import Transakcja  # Upewnij się, że ten moduł istnieje
import customtkinter as ctk
from tkinter import ttk

class BudzetGUIView:
    def __init__(self, controller):
        self.controller = controller

        # Ustawienia customtkinter
        ctk.set_appearance_mode("System")  # lub "Dark", "Light"
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Aplikacja Budżetowa")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        self.create_main_menu()
        self.create_initial_frames()

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

        # Widok Menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Widok", menu=view_menu)
        view_menu.add_command(label="Przełącz na tryb tekstowy (curses)", command=self.switch_to_curses)

    def create_initial_frames(self):
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.show_welcome_screen()

    def show_welcome_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Witaj w aplikacji budżetowej!",
                     font=("Helvetica", 18, "bold")).pack(pady=30)

        ctk.CTkButton(self.main_frame, text="Zaloguj się", command=self.show_login_form, width=200).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Zarejestruj się", command=self.show_register_form, width=200).pack(pady=10)

    def show_login_form(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Logowanie", font=("Helvetica", 16, "bold")).pack(pady=20)
        login_frame = ctk.CTkFrame(self.main_frame)
        login_frame.pack(pady=20)

        ctk.CTkLabel(login_frame, text="Login:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        login_entry = ctk.CTkEntry(login_frame)
        login_entry.grid(row=0, column=1, pady=5, padx=5)

        ctk.CTkLabel(login_frame, text="Hasło:", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        password_entry = ctk.CTkEntry(login_frame, show='*')
        password_entry.grid(row=1, column=1, pady=5, padx=5)

        message_label = ctk.CTkLabel(self.main_frame, text="", font=("Helvetica", 12), text_color="red")
        message_label.pack(pady=5)

        def attempt_login():
            login = login_entry.get()
            password = password_entry.get()
            if self.controller.model.zaloguj(login, password):
                message_label.configure(text="Zalogowano pomyślnie", text_color="green")
                self.update_main_frame_after_login()
            else:
                message_label.configure(text="Nieprawidłowy login lub hasło", text_color="red")

        ctk.CTkButton(self.main_frame, text="Zaloguj", command=attempt_login, width=200).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Powrót", command=self.show_welcome_screen, width=200).pack(pady=10)

    def show_register_form(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Rejestracja", font=("Helvetica", 16, "bold")).pack(pady=20)
        register_frame = ctk.CTkFrame(self.main_frame)
        register_frame.pack(pady=20)

        ctk.CTkLabel(register_frame, text="Nowy login:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        login_entry = ctk.CTkEntry(register_frame)
        login_entry.grid(row=0, column=1, pady=5, padx=5)

        ctk.CTkLabel(register_frame, text="Hasło:", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        password_entry = ctk.CTkEntry(register_frame, show='*')
        password_entry.grid(row=1, column=1, pady=5, padx=5)

        message_label = ctk.CTkLabel(self.main_frame, text="", font=("Helvetica", 12), text_color="red")
        message_label.pack(pady=5)

        def attempt_register():
            login = login_entry.get()
            password = password_entry.get()
            if self.controller.model.zarejestruj(login, password):
                message_label.configure(text="Rejestracja udana. Możesz się teraz zalogować.", text_color="green")
                self.show_login_form()
            else:
                message_label.configure(text="Użytkownik o takim loginie już istnieje", text_color="red")

        ctk.CTkButton(self.main_frame, text="Zarejestruj", command=attempt_register, width=200).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Powrót", command=self.show_welcome_screen, width=200).pack(pady=10)

    def update_main_frame_after_login(self):
        # Usunięcie starej ramki
        self.main_frame.pack_forget()

        # Główna ramka dla zalogowanego użytkownika
        self.logged_in_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.logged_in_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.logged_in_frame,
                     text=f"Witaj, {self.controller.model.zalogowany_uzytkownik}!",
                     font=("Helvetica", 16)).pack(pady=20)

        balance = self.controller.model.oblicz_saldo()
        ctk.CTkLabel(self.logged_in_frame, text=f"Saldo: {balance:.2f} zł", font=("Helvetica", 14)).pack(pady=10)

        self.buttons_frame = ctk.CTkFrame(self.logged_in_frame, corner_radius=10)
        self.buttons_frame.pack(pady=20)

        ctk.CTkButton(self.buttons_frame, text="Dodaj Transakcję", command=self.show_add_transaction, width=200).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(self.buttons_frame, text="Pokaż Transakcje", command=self.show_transactions, width=200).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(self.buttons_frame, text="Raport Wydatków", command=self.show_expense_report, width=200).grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(self.buttons_frame, text="Raport Przychodów", command=self.show_income_report, width=200).grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(self.buttons_frame, text="Wykres Wydatków", command=self.show_expense_chart, width=200).grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkButton(self.buttons_frame, text="Wykres Przychodów", command=self.show_income_chart, width=200).grid(row=2, column=1, padx=10, pady=10)
        ctk.CTkButton(self.buttons_frame, text="Ustaw Limity", command=self.set_limit, width=200).grid(row=3, column=0, padx=10, pady=10)
        ctk.CTkButton(self.buttons_frame, text="Pokaż Limity", command=self.show_limits, width=200).grid(row=3, column=1, padx=10, pady=10)

        # Ramka na dynamiczną zawartość
        self.content_frame = ctk.CTkFrame(self.logged_in_frame, corner_radius=10)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def logout(self):
        if hasattr(self, 'logged_in_frame'):
            self.logged_in_frame.pack_forget()
        self.controller.model.zalogowany_uzytkownik = None
        self.create_initial_frames()

    def show_add_transaction(self):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Kwota:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        amount_entry = ctk.CTkEntry(frame)
        amount_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="Kategoria:", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        category_entry = ctk.CTkEntry(frame)
        category_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="Typ:", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar(value="wydatek")
        type_combobox = ctk.CTkComboBox(frame, values=["wydatek", "przychód"], variable=type_var)
        type_combobox.grid(row=2, column=1, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="Opis:", font=("Helvetica", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        description_entry = ctk.CTkEntry(frame)
        description_entry.grid(row=3, column=1, pady=5, sticky="ew")

        message_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 12), text_color="red")
        message_label.grid(row=5, column=0, columnspan=2, pady=10)

        frame.columnconfigure(1, weight=1)

        def add_transaction():
            try:
                amount = float(amount_entry.get())
                category = category_entry.get().strip()
                transaction_type = type_var.get()
                description = description_entry.get().strip()

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
                message_label.configure(text="Transakcja dodana pomyślnie", text_color="green")
                self.show_transactions()  # Odśwież listę transakcji
            except ValueError as ve:
                message_label.configure(text=f"Błąd: {ve}", text_color="red")
            except Exception as e:
                message_label.configure(text=f"Nieoczekiwany błąd: {e}", text_color="red")

        ctk.CTkButton(frame, text="Dodaj", command=add_transaction).grid(row=4, column=0, columnspan=2, pady=20)

    def show_transactions(self):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Kwota", "Kategoria", "Typ", "Opis", "Data")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill="both", expand=True)

        for transaction in self.controller.model.transakcje:
            tree.insert("", "end", values=(transaction.kwota, transaction.kategoria, transaction.typ, transaction.opis, transaction.data))

    def show_expense_report(self):
        report = self.controller.model.generuj_raport_wydatkow()
        self.show_report("Raport wydatków", report)

    def show_income_report(self):
        report = self.controller.model.generuj_raport_przychodow()
        self.show_report("Raport przychodów", report)

    def show_report(self, title, report):
        self.clear_content_frame()
        if not report:
            frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
            frame.pack(fill="both", expand=True, padx=10, pady=10)
            ctk.CTkLabel(frame, text="Brak danych do wyświetlenia raportu.", font=("Helvetica", 12)).pack(pady=20)
            return

        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frame, text=title, font=("Helvetica", 16, "bold")).pack(pady=10)

        columns = ("Kategoria", "Kwota")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill="both", expand=True)

        for category, amount in report.items():
            tree.insert("", "end", values=(category, f"{amount:.2f} zł"))

    def show_expense_chart(self):
        report = self.controller.model.generuj_raport_wydatkow()
        self.show_chart("Wykres wydatków", report)

    def show_income_chart(self):
        report = self.controller.model.generuj_raport_przychodow()
        self.show_chart("Wykres przychodów", report)

    def show_chart(self, title, data):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text=title, font=("Helvetica", 16, "bold")).pack(pady=10)

        if not data:
            ctk.CTkLabel(frame, text="Brak danych do wyświetlenia wykresu.", font=("Helvetica", 12)).pack(pady=20)
            return

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title(title)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def set_limit(self):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Ustaw Limit", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(frame, text="Kategoria:", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        category_entry = ctk.CTkEntry(frame)
        category_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="Limit (zł):", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        limit_entry = ctk.CTkEntry(frame)
        limit_entry.grid(row=2, column=1, pady=5, sticky="ew")

        message_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 12), text_color="red")
        message_label.grid(row=4, column=0, columnspan=2, pady=10)

        frame.columnconfigure(1, weight=1)

        def save_limit():
            category = category_entry.get().strip()
            limit_str = limit_entry.get().strip()
            if not category:
                message_label.configure(text="Kategoria nie może być pusta", text_color="red")
                return
            try:
                limit = float(limit_str)
                self.controller.model.ustaw_limit(category, limit)
                message_label.configure(text=f"Ustawiono limit {limit:.2f} zł dla kategorii '{category}'", text_color="green")
            except ValueError:
                message_label.configure(text="Nieprawidłowa wartość limitu", text_color="red")

        ctk.CTkButton(frame, text="Zapisz", command=save_limit).grid(row=3, column=0, columnspan=2, pady=20)

    def show_limits(self):
        limits = self.controller.model.limity
        self.show_report("Limity budżetowe", limits)

    def export_to_csv(self):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Eksport do CSV", font=("Helvetica", 16, "bold")).pack(pady=20)

        message_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 12))
        message_label.pack(pady=10)

        try:
            self.controller.model.eksportuj_do_csv()
            message_label.configure(text="Dane zostały wyeksportowane do pliku CSV", text_color="green")
        except Exception as e:
            message_label.configure(text=f"Nie udało się wyeksportować danych: {e}", text_color="red")

    def import_from_csv(self):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Import z CSV", font=("Helvetica", 16, "bold")).pack(pady=20)

        message_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 12))
        message_label.pack(pady=10)

        try:
            if self.controller.model.importuj_z_csv():
                message_label.configure(text="Dane zostały zaimportowane z pliku CSV", text_color="green")
                self.show_transactions()
            else:
                message_label.configure(text="Nie udało się zaimportować danych z pliku CSV", text_color="red")
        except Exception as e:
            message_label.configure(text=f"Nie udało się zaimportować danych: {e}", text_color="red")

    def switch_to_curses(self):
        self.root.destroy()
        from curses_view import BudzetCursesView  # Upewnij się, że ten moduł istnieje
        new_view = BudzetCursesView()
        new_view.controller = self.controller
        self.controller.view = new_view
        self.controller.view.run()

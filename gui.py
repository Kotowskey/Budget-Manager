import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog, messagebox

class BudzetGUIView:
    def __init__(self, controller):
        self.controller = controller
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Aplikacja Budżetowa")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.create_initial_frames()

    def run(self):
        self.root.mainloop()

    def create_initial_frames(self):
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.show_welcome_screen()

    def show_welcome_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.main_frame,
            text="Budget Manager",
            font=("Helvetica", 18, "bold")
        ).pack(pady=30)

        ctk.CTkButton(
            self.main_frame,
            text="Zaloguj się",
            command=self.show_login_form,
            width=200
        ).pack(pady=10)

        ctk.CTkButton(
            self.main_frame,
            text="Zarejestruj się",
            command=self.show_register_form,
            width=200
        ).pack(pady=10)

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
            if self.controller.service.zaloguj(login, password):
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
            if self.controller.service.zarejestruj(login, password):
                message_label.configure(text="Rejestracja udana. Możesz się teraz zalogować.", text_color="green")
                self.show_login_form()
            else:
                message_label.configure(text="Użytkownik o takim loginie już istnieje", text_color="red")

        ctk.CTkButton(self.main_frame, text="Zarejestruj", command=attempt_register, width=200).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Powrót", command=self.show_welcome_screen, width=200).pack(pady=10)

    def update_main_frame_after_login(self):
        self.main_frame.pack_forget()
        self.logged_in_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.logged_in_frame.pack(fill="both", expand=True, padx=20, pady=20)

        user = self.controller.model.zalogowany_uzytkownik or ""
        ctk.CTkLabel(
            self.logged_in_frame,
            text=f"Witaj, {user}!",
            font=("Helvetica", 16)
        ).pack(pady=20)

        balance = self.controller.service.oblicz_saldo()
        self.balance_label = ctk.CTkLabel(self.logged_in_frame, text=f"Saldo: {balance:.2f} zł", font=("Helvetica", 14))
        self.balance_label.pack(pady=10)

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
        ctk.CTkButton(self.buttons_frame, text="Import CSV", command=self.import_from_csv, width=200).grid(row=4, column=0, padx=10, pady=10)
        ctk.CTkButton(self.buttons_frame, text="Eksport CSV", command=self.export_to_csv, width=200).grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkButton(
            self.buttons_frame,
            text="Wyloguj się",
            command=self.logout,
            width=200,
            fg_color="red",
            hover_color="darkred"
        ).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

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

        ctk.CTkLabel(frame, text="Data (YYYY-MM-DD):", font=("Helvetica", 12)).grid(row=4, column=0, sticky=tk.W, pady=5)
        date_entry = ctk.CTkEntry(frame)
        date_entry.grid(row=4, column=1, pady=5, sticky="ew")
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        message_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 12), text_color="red")
        message_label.grid(row=6, column=0, columnspan=2, pady=10)

        frame.columnconfigure(1, weight=1)

        def add_transaction():
            try:
                amount = float(amount_entry.get())
                category = category_entry.get().strip()
                transaction_type = type_var.get()
                description = description_entry.get().strip()
                date_str = date_entry.get().strip()

                if not category:
                    raise ValueError("Kategoria nie może być pusta")

                try:
                    datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    date_formatted = datetime_obj.strftime('%Y-%m-%d')
                except ValueError:
                    raise ValueError("Nieprawidłowy format daty. Użyj YYYY-MM-DD.")

                if transaction_type.lower() == 'wydatek' and not self.controller.service.sprawdz_limit(category, amount):
                    raise ValueError(f"Przekroczono limit dla kategorii '{category}'")

                from model import Transakcja
                transaction = Transakcja(
                    kwota=amount,
                    kategoria=category,
                    typ=transaction_type,
                    opis=description,
                    data=date_formatted
                )
                self.controller.service.dodaj_transakcje(transaction)
                self.balance_label.configure(text=f"Saldo: {self.controller.service.oblicz_saldo():.2f} zł")
                message_label.configure(text="Transakcja dodana pomyślnie", text_color="green")
                self.show_transactions()
            except ValueError as ve:
                message_label.configure(text=f"Błąd: {ve}", text_color="red")
            except Exception as e:
                message_label.configure(text=f"Nieoczekiwany błąd: {e}", text_color="red")

        ctk.CTkButton(frame, text="Dodaj", command=add_transaction).grid(row=5, column=0, columnspan=2, pady=20)

    def show_transactions(self):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        buttons_frame = ctk.CTkFrame(frame)
        buttons_frame.pack(pady=10)

        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Usuń Wybraną Transakcję",
            command=lambda: self.delete_selected_transaction(tree),
            fg_color="red",
            hover_color="darkred",
            width=200
        )
        delete_button.pack(side=tk.LEFT, padx=10)

        edit_button = ctk.CTkButton(
            buttons_frame,
            text="Edytuj Wybraną Transakcję",
            command=lambda: self.edit_selected_transaction(tree),
            fg_color="orange",
            hover_color="darkorange",
            width=200
        )
        edit_button.pack(side=tk.LEFT, padx=10)

        filter_button = ctk.CTkButton(
            buttons_frame,
            text="Filtruj Transakcje",
            command=self.show_filter_transactions,
            fg_color="blue",
            hover_color="darkblue",
            width=200
        )
        filter_button.pack(side=tk.LEFT, padx=10)

        columns = ("Kwota", "Kategoria", "Typ", "Opis", "Data")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill="both", expand=True)

        self.transaction_id_map = {}
        for index, transaction in enumerate(self.controller.model.transakcje):
            item_id = tree.insert("", "end", values=(
                f"{transaction.kwota:.2f} zł",
                transaction.kategoria,
                transaction.typ.capitalize(),
                transaction.opis,
                transaction.data
            ))
            self.transaction_id_map[item_id] = index

        self.balance_label.configure(text=f"Saldo: {self.controller.service.oblicz_saldo():.2f} zł")

    def delete_selected_transaction(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać transakcję do usunięcia.")
            return
        item_id = selected_item[0]
        index = self.transaction_id_map.get(item_id)
        if index is None:
            messagebox.showerror("Błąd", "Nie można znaleźć wybranej transakcji.")
            return

        confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć wybraną transakcję?")
        if not confirm:
            return

        success = self.controller.service.usun_transakcje(index)
        if success:
            messagebox.showinfo("Sukces", "Transakcja została pomyślnie usunięta.")
            self.show_transactions()
            self.balance_label.configure(text=f"Saldo: {self.controller.service.oblicz_saldo():.2f} zł")
        else:
            messagebox.showerror("Błąd", "Nie udało się usunąć transakcji.")

    def edit_selected_transaction(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać transakcję do edycji.")
            return
        item_id = selected_item[0]
        index = self.transaction_id_map.get(item_id)
        if index is None:
            messagebox.showerror("Błąd", "Nie można znaleźć wybranej transakcji.")
            return

        transaction = self.controller.model.transakcje[index]

        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edytuj Transakcję")
        edit_window.geometry("400x400")

        frame = ctk.CTkFrame(edit_window, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Kwota:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        amount_entry = ctk.CTkEntry(frame)
        amount_entry.grid(row=0, column=1, pady=5, sticky="ew")
        amount_entry.insert(0, f"{transaction.kwota:.2f}")

        ctk.CTkLabel(frame, text="Kategoria:", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        category_entry = ctk.CTkEntry(frame)
        category_entry.grid(row=1, column=1, pady=5, sticky="ew")
        category_entry.insert(0, transaction.kategoria)

        ctk.CTkLabel(frame, text="Typ:", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        from tkinter import StringVar
        type_var = StringVar(value=transaction.typ)
        type_combobox = ctk.CTkComboBox(frame, values=["wydatek", "przychód"], variable=type_var)
        type_combobox.grid(row=2, column=1, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="Opis:", font=("Helvetica", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        description_entry = ctk.CTkEntry(frame)
        description_entry.grid(row=3, column=1, pady=5, sticky="ew")
        description_entry.insert(0, transaction.opis)

        ctk.CTkLabel(frame, text="Data (YYYY-MM-DD):", font=("Helvetica", 12)).grid(row=4, column=0, sticky=tk.W, pady=5)
        date_entry = ctk.CTkEntry(frame)
        date_entry.grid(row=4, column=1, pady=5, sticky="ew")
        date_entry.insert(0, transaction.data)

        message_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 12), text_color="red")
        message_label.grid(row=6, column=0, columnspan=2, pady=10)

        frame.columnconfigure(1, weight=1)

        def save_changes():
            try:
                amount = float(amount_entry.get())
                category = category_entry.get().strip()
                transaction_type = type_var.get()
                description = description_entry.get().strip()
                date_str = date_entry.get().strip()

                if not category:
                    raise ValueError("Kategoria nie może być pusta")

                try:
                    datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    date_formatted = datetime_obj.strftime('%Y-%m-%d')
                except ValueError:
                    raise ValueError("Nieprawidłowy format daty. Użyj YYYY-MM-DD.")

                if transaction_type.lower() == 'wydatek' and not self.controller.service.sprawdz_limit(category, amount):
                    raise ValueError(f"Przekroczono limit dla kategorii '{category}'")

                from model import Transakcja
                updated_transaction = Transakcja(
                    kwota=amount,
                    kategoria=category,
                    typ=transaction_type,
                    opis=description,
                    data=date_formatted
                )
                success = self.controller.service.edytuj_transakcje(index, updated_transaction)
                if success:
                    message_label.configure(text="Transakcja zaktualizowana pomyślnie", text_color="green")
                    self.balance_label.configure(text=f"Saldo: {self.controller.service.oblicz_saldo():.2f} zł")
                    self.show_transactions()
                    edit_window.destroy()
                else:
                    message_label.configure(text="Nie udało się zaktualizować transakcji", text_color="red")
            except ValueError as ve:
                message_label.configure(text=f"Błąd: {ve}", text_color="red")
            except Exception as e:
                message_label.configure(text=f"Nieoczekiwany błąd: {e}", text_color="red")

        ctk.CTkButton(frame, text="Zapisz Zmiany", command=save_changes).grid(row=5, column=0, columnspan=2, pady=20)

    def show_expense_report(self):
        report = self.controller.service.generuj_raport_wydatkow()
        self.show_report("Raport wydatków", report)

    def show_income_report(self):
        report = self.controller.service.generuj_raport_przychodow()
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
        report = self.controller.service.generuj_raport_wydatkow()
        self.show_chart("Wykres wydatków", report)

    def show_income_chart(self):
        report = self.controller.service.generuj_raport_przychodow()
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
                self.controller.service.ustaw_limit(category, limit)
                message_label.configure(text=f"Ustawiono limit {limit:.2f} zł dla kategorii '{category}'", text_color="green")
            except ValueError:
                message_label.configure(text="Nieprawidłowa wartość limitu", text_color="red")

        ctk.CTkButton(frame, text="Zapisz", command=save_limit).grid(row=3, column=0, columnspan=2, pady=20)

    def show_limits(self):
        self.clear_content_frame()
        limits = self.controller.model.limity
        if not limits:
            frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
            frame.pack(fill="both", expand=True, padx=10, pady=10)
            ctk.CTkLabel(frame, text="Brak ustawionych limitów.", font=("Helvetica", 12)).pack(pady=20)
            return

        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frame, text="Limity Budżetowe", font=("Helvetica", 16, "bold")).pack(pady=10)

        columns = ("Kategoria", "Limit (zł)")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill="both", expand=True)

        for kategoria, limit in limits.items():
            tree.insert("", "end", values=(kategoria, f"{limit:.2f} zł"))

        buttons_frame = ctk.CTkFrame(frame)
        buttons_frame.pack(pady=10)

        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Usuń Wybrany Limit",
            command=lambda: self.delete_selected_limit(tree),
            fg_color="red",
            hover_color="darkred",
            width=200
        )
        delete_button.pack(side=tk.LEFT, padx=10)

    def delete_selected_limit(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać limit do usunięcia.")
            return
        item = tree.item(selected_item)
        kategoria = item['values'][0]
        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć limit dla kategorii '{kategoria}'?")
        if not confirm:
            return

        success = self.controller.service.usun_limit(kategoria)
        if success:
            messagebox.showinfo("Sukces", f"Limit dla kategorii '{kategoria}' został usunięty.")
            self.show_limits()
        else:
            messagebox.showerror("Błąd", f"Nie udało się usunąć limitu dla kategorii '{kategoria}'.")

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Eksportuj do CSV"
        )
        if not file_path:
            return
        try:
            self.controller.service.eksportuj_do_csv(file_path)
            messagebox.showinfo("Sukces", "Dane zostały wyeksportowane do pliku CSV.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyeksportować danych: {e}")

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Importuj z CSV"
        )
        if not file_path:
            return
        try:
            if self.controller.service.importuj_z_csv(file_path):
                messagebox.showinfo("Sukces", "Dane zostały zaimportowane z pliku CSV.")
                self.show_transactions()
                self.balance_label.configure(text=f"Saldo: {self.controller.service.oblicz_saldo():.2f} zł")
            else:
                messagebox.showwarning("Ostrzeżenie", "Nie udało się zaimportować danych z pliku CSV.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zaimportować danych: {e}")

    def show_filter_transactions(self):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Filtruj Transakcje", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(frame, text="Data początkowa (YYYY-MM-DD):", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        start_date_entry = ctk.CTkEntry(frame)
        start_date_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ctk.CTkLabel(frame, text="Data końcowa (YYYY-MM-DD):", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        end_date_entry = ctk.CTkEntry(frame)
        end_date_entry.grid(row=2, column=1, pady=5, sticky="ew")

        message_label = ctk.CTkLabel(frame, text="", font=("Helvetica", 12), text_color="red")
        message_label.grid(row=4, column=0, columnspan=2, pady=10)
        frame.columnconfigure(1, weight=1)

        def apply_filter():
            start_date = start_date_entry.get().strip()
            end_date = end_date_entry.get().strip()
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
                filtered_transactions = self.filtruj_transakcje_po_dacie(start_date, end_date)
                if not filtered_transactions:
                    message_label.configure(text="Brak transakcji w podanym zakresie dat.", text_color="orange")
                else:
                    self.display_filtered_transactions(filtered_transactions)
            except ValueError:
                message_label.configure(text="Nieprawidłowy format daty. Użyj YYYY-MM-DD.", text_color="red")
            except Exception as e:
                message_label.configure(text=f"Nieoczekiwany błąd: {e}", text_color="red")

        ctk.CTkButton(frame, text="Filtruj", command=apply_filter).grid(row=3, column=0, columnspan=2, pady=20)

    def filtruj_transakcje_po_dacie(self, start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        return [
            t for t in self.controller.model.transakcje
            if start_date <= datetime.strptime(t.data, '%Y-%m-%d').date() <= end_date
        ]

    def display_filtered_transactions(self, transactions):
        self.clear_content_frame()
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        buttons_frame = ctk.CTkFrame(frame)
        buttons_frame.pack(pady=10)

        back_button = ctk.CTkButton(
            buttons_frame,
            text="Powrót do Transakcji",
            command=self.show_transactions,
            fg_color="blue",
            hover_color="darkblue",
            width=200
        )
        back_button.pack(side=tk.LEFT, padx=10)

        columns = ("Kwota", "Kategoria", "Typ", "Opis", "Data")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill="both", expand=True)

        for t in transactions:
            tree.insert(
                "",
                "end",
                values=(f"{t.kwota:.2f} zł", t.kategoria, t.typ.capitalize(), t.opis, t.data)
            )

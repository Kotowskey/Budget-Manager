# view.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
from typing import Optional, Tuple, Dict
from model import Transakcja

class BudzetGUIView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplikacja Budżetowa")
        self.controller = None  # Będzie ustawiony przez kontroler
        self.setup_main_window()

    def set_controller(self, controller):
        self.controller = controller

    def setup_main_window(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_frame()

        welcome_label = tk.Label(self.main_frame, text="Witamy w Aplikacji Budżetowej", font=("Arial", 16))
        welcome_label.pack(pady=20)

        login_button = tk.Button(self.main_frame, text="Zaloguj się", width=20, command=self.show_login)
        login_button.pack(pady=10)

        register_button = tk.Button(self.main_frame, text="Zarejestruj się", width=20, command=self.show_register)
        register_button.pack(pady=10)

        exit_button = tk.Button(self.main_frame, text="Wyjście", width=20, command=self.root.quit)
        exit_button.pack(pady=10)

    def show_login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Logowanie")

        tk.Label(login_window, text="Login:").grid(row=0, column=0, padx=10, pady=10)
        login_entry = tk.Entry(login_window)
        login_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(login_window, text="Hasło:").grid(row=1, column=0, padx=10, pady=10)
        haslo_entry = tk.Entry(login_window, show='*')
        haslo_entry.grid(row=1, column=1, padx=10, pady=10)

        def submit_login():
            login = login_entry.get()
            haslo = haslo_entry.get()
            if login and haslo:
                self.controller.handle_login(login, haslo)
                login_window.destroy()
            else:
                messagebox.showerror("Błąd", "Proszę wprowadzić zarówno login, jak i hasło.")

        submit_button = tk.Button(login_window, text="Zaloguj", command=submit_login)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def show_register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Rejestracja")

        tk.Label(register_window, text="Wybierz login:").grid(row=0, column=0, padx=10, pady=10)
        login_entry = tk.Entry(register_window)
        login_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(register_window, text="Wybierz hasło:").grid(row=1, column=0, padx=10, pady=10)
        haslo_entry = tk.Entry(register_window, show='*')
        haslo_entry.grid(row=1, column=1, padx=10, pady=10)

        def submit_register():
            login = login_entry.get()
            haslo = haslo_entry.get()
            if login and haslo:
                self.controller.handle_register(login, haslo)
                register_window.destroy()
            else:
                messagebox.showerror("Błąd", "Proszę wprowadzić zarówno login, jak i hasło.")

        submit_button = tk.Button(register_window, text="Zarejestruj", command=submit_register)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def display_message(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def show_main_menu(self):
        self.clear_frame()

        main_menu_label = tk.Label(self.main_frame, text="Główne Menu", font=("Arial", 14))
        main_menu_label.pack(pady=20)

        transactions_button = tk.Button(self.main_frame, text="Transakcje", width=25, command=self.controller.show_transactions)
        transactions_button.pack(pady=10)

        summaries_button = tk.Button(self.main_frame, text="Podsumowania", width=25, command=self.controller.show_summaries)
        summaries_button.pack(pady=10)

        limits_button = tk.Button(self.main_frame, text="Limity", width=25, command=self.controller.show_limits)
        limits_button.pack(pady=10)

        import_export_button = tk.Button(self.main_frame, text="Import/Eksport", width=25, command=self.controller.show_import_export)
        import_export_button.pack(pady=10)

        logout_button = tk.Button(self.main_frame, text="Wyloguj się", width=25, command=self.controller.handle_logout)
        logout_button.pack(pady=10)

    def show_transactions(self):
        self.clear_frame()

        transactions_label = tk.Label(self.main_frame, text="Transakcje", font=("Arial", 14))
        transactions_label.pack(pady=10)

        columns = ("#1", "#2", "#3", "#4", "#5")
        self.trans_table = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        self.trans_table.heading("#1", text="Kwota")
        self.trans_table.heading("#2", text="Kategoria")
        self.trans_table.heading("#3", text="Typ")
        self.trans_table.heading("#4", text="Opis")
        self.trans_table.heading("#5", text="Data")

        self.trans_table.pack(pady=10, fill=tk.BOTH, expand=True)

        self.controller.refresh_transactions_view()

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Dodaj Transakcję", command=self.controller.show_add_transaction)
        add_button.grid(row=0, column=0, padx=5)

        edit_button = tk.Button(button_frame, text="Edytuj Transakcję", command=self.controller.edit_selected_transaction)
        edit_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(button_frame, text="Usuń Transakcję", command=self.controller.delete_selected_transaction)
        delete_button.grid(row=0, column=2, padx=5)

        back_button = tk.Button(self.main_frame, text="Wróć do Menu", command=self.show_main_menu)
        back_button.pack(pady=5)

    def refresh_transactions_view(self, transakcje=None):
        for i in self.trans_table.get_children():
            self.trans_table.delete(i)
        if transakcje is None:
            transakcje = self.controller.model.transakcje
        for idx, t in enumerate(transakcje):
            self.trans_table.insert("", "end", iid=idx, values=(t.kwota, t.kategoria, t.typ, t.opis, t.data))

    def show_add_transaction(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Dodaj Transakcję")

        tk.Label(add_window, text="Kwota:").grid(row=0, column=0, padx=10, pady=5)
        kwota_entry = tk.Entry(add_window)
        kwota_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Kategoria:").grid(row=1, column=0, padx=10, pady=5)
        kategoria_entry = tk.Entry(add_window)
        kategoria_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Typ:").grid(row=2, column=0, padx=10, pady=5)
        typ_var = tk.StringVar(value="przychód")
        typ_menu = tk.OptionMenu(add_window, typ_var, "przychód", "wydatek")
        typ_menu.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Opis:").grid(row=3, column=0, padx=10, pady=5)
        opis_entry = tk.Entry(add_window)
        opis_entry.grid(row=3, column=1, padx=10, pady=5)

        def submit():
            try:
                kwota = float(kwota_entry.get())
                kategoria = kategoria_entry.get()
                typ = typ_var.get()
                opis = opis_entry.get()
                data = datetime.now().strftime('%Y-%m-%d')
                transakcja = {
                    'kwota': kwota,
                    'kategoria': kategoria,
                    'typ': typ,
                    'opis': opis,
                    'data': data
                }
                self.controller.add_transaction(transakcja)
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowa kwota.")

        submit_button = tk.Button(add_window, text="Dodaj", command=submit)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def edit_selected_transaction(self):
        selected = self.trans_table.selection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać transakcję do edycji.")
            return
        indeks = int(selected[0])
        transakcja = self.controller.model.transakcje[indeks]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edytuj Transakcję")

        tk.Label(edit_window, text="Kwota:").grid(row=0, column=0, padx=10, pady=5)
        kwota_entry = tk.Entry(edit_window)
        kwota_entry.insert(0, transakcja.kwota)
        kwota_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Kategoria:").grid(row=1, column=0, padx=10, pady=5)
        kategoria_entry = tk.Entry(edit_window)
        kategoria_entry.insert(0, transakcja.kategoria)
        kategoria_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Typ:").grid(row=2, column=0, padx=10, pady=5)
        typ_var = tk.StringVar(value=transakcja.typ)
        typ_menu = tk.OptionMenu(edit_window, typ_var, "przychód", "wydatek")
        typ_menu.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Opis:").grid(row=3, column=0, padx=10, pady=5)
        opis_entry = tk.Entry(edit_window)
        opis_entry.insert(0, transakcja.opis)
        opis_entry.grid(row=3, column=1, padx=10, pady=5)

        def submit_edit():
            try:
                kwota = float(kwota_entry.get())
                kategoria = kategoria_entry.get()
                typ = typ_var.get()
                opis = opis_entry.get()
                data = transakcja.data  # Data nie jest edytowana
                nowa_transakcja = {
                    'kwota': kwota,
                    'kategoria': kategoria,
                    'typ': typ,
                    'opis': opis,
                    'data': data
                }
                self.controller.edit_transaction(indeks, nowa_transakcja)
                edit_window.destroy()
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowa kwota.")

        submit_button = tk.Button(edit_window, text="Zapisz", command=submit_edit)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def delete_selected_transaction(self):
        selected = self.trans_table.selection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać transakcję do usunięcia.")
            return
        indeks = int(selected[0])
        confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć wybraną transakcję?")
        if confirm:
            self.controller.delete_transaction(indeks)

    def show_summaries(self):
        self.clear_frame()

        summaries_label = tk.Label(self.main_frame, text="Podsumowania", font=("Arial", 14))
        summaries_label.pack(pady=10)

        saldo = self.controller.model.oblicz_saldo()
        saldo_label = tk.Label(self.main_frame, text=f"Saldo: {saldo} zł", font=("Arial", 12))
        saldo_label.pack(pady=5)

        raport_wydatkow = self.controller.model.generuj_raport_wydatkow()
        raport_przychodow = self.controller.model.generuj_raport_przychodow()

        raport_frame = tk.Frame(self.main_frame)
        raport_frame.pack(pady=10)

        wydatki_label = tk.Label(raport_frame, text="Raport Wydatków", font=("Arial", 12, "underline"))
        wydatki_label.grid(row=0, column=0, padx=10, pady=5)

        for idx, (kategoria, kwota) in enumerate(raport_wydatkow.items(), start=1):
            tk.Label(raport_frame, text=kategoria).grid(row=idx, column=0, padx=10, sticky='w')
            tk.Label(raport_frame, text=f"{kwota} zł").grid(row=idx, column=1, padx=10, sticky='w')

        przychody_label = tk.Label(raport_frame, text="Raport Przychodów", font=("Arial", 12, "underline"))
        przychody_label.grid(row=0, column=2, padx=10, pady=5)

        for idx, (kategoria, kwota) in enumerate(raport_przychodow.items(), start=1):
            tk.Label(raport_frame, text=kategoria).grid(row=idx, column=2, padx=10, sticky='w')
            tk.Label(raport_frame, text=f"{kwota} zł").grid(row=idx, column=3, padx=10, sticky='w')

        back_button = tk.Button(self.main_frame, text="Wróć do Menu", command=self.show_main_menu)
        back_button.pack(pady=10)

    def show_limits(self):
        self.clear_frame()

        limits_label = tk.Label(self.main_frame, text="Limity", font=("Arial", 14))
        limits_label.pack(pady=10)

        self.limits_table = ttk.Treeview(self.main_frame, columns=("#1", "#2"), show='headings')
        self.limits_table.heading("#1", text="Kategoria")
        self.limits_table.heading("#2", text="Limit (zł)")
        self.limits_table.pack(pady=10, fill=tk.BOTH, expand=True)

        self.controller.refresh_limits_view()

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)

        add_limit_button = tk.Button(button_frame, text="Ustaw Limit", command=self.controller.show_set_limit)
        add_limit_button.grid(row=0, column=0, padx=5)

        delete_limit_button = tk.Button(button_frame, text="Usuń Limit", command=self.controller.delete_selected_limit)
        delete_limit_button.grid(row=0, column=1, padx=5)

        back_button = tk.Button(self.main_frame, text="Wróć do Menu", command=self.show_main_menu)
        back_button.pack(pady=5)

    def refresh_limits_view(self, limity=None):
        for i in self.limits_table.get_children():
            self.limits_table.delete(i)
        if limity is None:
            limity = self.controller.model.limity
        for kategoria, limit in limity.items():
            self.limits_table.insert("", "end", values=(kategoria, f"{limit} zł"))

    def show_set_limit(self):
        set_limit_window = tk.Toplevel(self.root)
        set_limit_window.title("Ustaw Limit Budżetowy")

        tk.Label(set_limit_window, text="Kategoria:").grid(row=0, column=0, padx=10, pady=5)
        kategoria_entry = tk.Entry(set_limit_window)
        kategoria_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(set_limit_window, text="Limit (zł):").grid(row=1, column=0, padx=10, pady=5)
        limit_entry = tk.Entry(set_limit_window)
        limit_entry.grid(row=1, column=1, padx=10, pady=5)

        def submit_limit():
            kategoria = kategoria_entry.get()
            try:
                limit = float(limit_entry.get())
                if kategoria and limit > 0:
                    self.controller.set_limit(kategoria, limit)
                    set_limit_window.destroy()
                else:
                    messagebox.showerror("Błąd", "Proszę wprowadzić poprawne dane.")
            except ValueError:
                messagebox.showerror("Błąd", "Limit musi być liczbą.")

        submit_button = tk.Button(set_limit_window, text="Ustaw Limit", command=submit_limit)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def delete_selected_limit(self):
        selected = self.limits_table.selection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać limit do usunięcia.")
            return
        kategoria = self.limits_table.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć limit dla kategorii '{kategoria}'?")
        if confirm:
            self.controller.delete_limit(kategoria)

    def show_import_export(self):
        self.clear_frame()

        import_export_label = tk.Label(self.main_frame, text="Import/Eksport", font=("Arial", 14))
        import_export_label.pack(pady=10)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)

        import_button = tk.Button(button_frame, text="Importuj z CSV", width=20, command=self.controller.import_transactions)
        import_button.grid(row=0, column=0, padx=10, pady=5)

        export_button = tk.Button(button_frame, text="Eksportuj do CSV", width=20, command=self.controller.export_transactions)
        export_button.grid(row=0, column=1, padx=10, pady=5)

        back_button = tk.Button(self.main_frame, text="Wróć do Menu", command=self.show_main_menu)
        back_button.pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

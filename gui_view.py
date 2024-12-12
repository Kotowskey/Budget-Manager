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
        self.root.geometry("800x600")
        
        self.create_main_menu()
        self.create_frames()
        
    def run(self):
        self.root.mainloop()
        
    def create_main_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Plik", menu=file_menu)
        file_menu.add_command(label="Wyloguj", command=self.logout)
        file_menu.add_command(label="Wyjście", command=self.root.quit)
        
        transactions_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Transakcje", menu=transactions_menu)
        transactions_menu.add_command(label="Dodaj transakcję", command=self.show_add_transaction)
        transactions_menu.add_command(label="Pokaż transakcje", command=self.show_transactions)
        
        summary_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Podsumowania", menu=summary_menu)
        summary_menu.add_command(label="Raport wydatków", command=self.show_expense_report)
        summary_menu.add_command(label="Raport przychodów", command=self.show_income_report)
        summary_menu.add_command(label="Wykres wydatków", command=self.show_expense_chart)
        summary_menu.add_command(label="Wykres przychodów", command=self.show_income_chart)
        
        limits_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Limity", menu=limits_menu)
        limits_menu.add_command(label="Ustaw limit", command=self.set_limit)
        limits_menu.add_command(label="Pokaż limity", command=self.show_limits)
        
        import_export_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Import/Eksport", menu=import_export_menu)
        import_export_menu.add_command(label="Eksportuj do CSV", command=self.export_to_csv)
        import_export_menu.add_command(label="Importuj z CSV", command=self.import_from_csv)
        
    def create_frames(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.welcome_label = ttk.Label(self.main_frame, text="Witaj w aplikacji budżetowej!", font=("Arial", 16))
        self.welcome_label.grid(row=0, column=0, pady=20)
        
        self.login_button = ttk.Button(self.main_frame, text="Zaloguj się", command=self.show_login)
        self.login_button.grid(row=1, column=0, pady=10)
        
        self.register_button = ttk.Button(self.main_frame, text="Zarejestruj się", command=self.show_register)
        self.register_button.grid(row=2, column=0, pady=10)
        
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
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.welcome_label = ttk.Label(self.main_frame, text=f"Witaj, {self.controller.model.zalogowany_uzytkownik}!", font=("Arial", 16))
        self.welcome_label.grid(row=0, column=0, pady=20)
        
        self.balance_label = ttk.Label(self.main_frame, text=f"Saldo: {self.controller.model.oblicz_saldo():.2f} zł", font=("Arial", 14))
        self.balance_label.grid(row=1, column=0, pady=10)
        
    def logout(self):
        self.controller.model.zalogowany_uzytkownik = None
        messagebox.showinfo("Wylogowanie", "Wylogowano pomyślnie")
        self.create_frames()
        
    def show_add_transaction(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Dodaj transakcję")
        
        ttk.Label(add_window, text="Kwota:").grid(row=0, column=0, padx=5, pady=5)
        amount_entry = ttk.Entry(add_window)
        amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Kategoria:").grid(row=1, column=0, padx=5, pady=5)
        category_entry = ttk.Entry(add_window)
        category_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Typ:").grid(row=2, column=0, padx=5, pady=5)
        type_var = tk.StringVar(value="wydatek")
        type_combobox = ttk.Combobox(add_window, textvariable=type_var, values=["wydatek", "przychód"])
        type_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Opis:").grid(row=3, column=0, padx=5, pady=5)
        description_entry = ttk.Entry(add_window)
        description_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def add_transaction():
            try:
                amount = float(amount_entry.get())
                category = category_entry.get()
                transaction_type = type_var.get()
                description = description_entry.get()
                
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
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowa kwota")
        
        ttk.Button(add_window, text="Dodaj", command=add_transaction).grid(row=4, column=0, columnspan=2, pady=10)
        
    def show_transactions(self):
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Lista transakcji")
        transactions_window.geometry("600x400")
        
        tree = ttk.Treeview(transactions_window, columns=("Kwota", "Kategoria", "Typ", "Opis", "Data"), show="headings")
        tree.heading("Kwota", text="Kwota")
        tree.heading("Kategoria", text="Kategoria")
        tree.heading("Typ", text="Typ")
        tree.heading("Opis", text="Opis")
        tree.heading("Data", text="Data")
        
        for transaction in self.controller.model.transakcje:
            tree.insert("", "end", values=(transaction.kwota, transaction.kategoria, transaction.typ, transaction.opis, transaction.data))
        
        tree.pack(expand=True, fill="both")
        
    def show_expense_report(self):
        report = self.controller.model.generuj_raport_wydatkow()
        self.show_report("Raport wydatków", report)
        
    def show_income_report(self):
        report = self.controller.model.generuj_raport_przychodow()
        self.show_report("Raport przychodów", report)
        
    def show_report(self, title, report):
        report_window = tk.Toplevel(self.root)
        report_window.title(title)
        report_window.geometry("400x300")
        
        tree = ttk.Treeview(report_window, columns=("Kategoria", "Kwota"), show="headings")
        tree.heading("Kategoria", text="Kategoria")
        tree.heading("Kwota", text="Kwota")
        
        for category, amount in report.items():
            tree.insert("", "end", values=(category, f"{amount:.2f} zł"))
        
        tree.pack(expand=True, fill="both")
        
    def show_expense_chart(self):
        report = self.controller.model.generuj_raport_wydatkow()
        self.show_chart("Wykres wydatków", report)
        
    def show_income_chart(self):
        report = self.controller.model.generuj_raport_przychodow()
        self.show_chart("Wykres przychodów", report)
        
    def show_chart(self, title, data):
        chart_window = tk.Toplevel(self.root)
        chart_window.title(title)
        chart_window.geometry("600x400")
        
        fig, ax = plt.subplots()
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def set_limit(self):
        category = simpledialog.askstring("Ustaw limit", "Podaj kategorię:")
        if category:
            limit = simpledialog.askfloat("Ustaw limit", f"Podaj limit dla kategorii {category}:")
            if limit is not None:
                self.controller.model.ustaw_limit(category, limit)
                messagebox.showinfo("Sukces", f"Ustawiono limit {limit:.2f} zł dla kategorii {category}")
                
    def show_limits(self):
        limits = self.controller.model.limity
        self.show_report("Limity budżetowe", limits)
        
    def export_to_csv(self):
        self.controller.model.eksportuj_do_csv()
        messagebox.showinfo("Eksport", "Dane zostały wyeksportowane do pliku CSV")
        
    def import_from_csv(self):
        if self.controller.model.importuj_z_csv():
            messagebox.showinfo("Import", "Dane zostały zaimportowane z pliku CSV")
            self.update_main_frame_after_login()
        else:
            messagebox.showerror("Błąd", "Nie udało się zaimportować danych z pliku CSV")

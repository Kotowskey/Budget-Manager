# controller.py
from model import BudzetModel, Transakcja
from view import BudzetGUIView
from tkinter import messagebox
from typing import Dict

class BudzetController:
    def __init__(self) -> None:
        self.model = BudzetModel()
        self.view = BudzetGUIView()
        self.view.set_controller(self)

    def run(self):
        self.view.run()

    def handle_login(self, login: str, haslo: str):
        if self.model.zaloguj(login, haslo):
            self.view.display_message("Sukces", f"Zalogowano jako {login}.")
            self.view.show_main_menu()
        else:
            self.view.display_message("Błąd", "Nieprawidłowy login lub hasło.")

    def handle_register(self, login: str, haslo: str):
        if self.model.zarejestruj(login, haslo):
            self.view.display_message("Sukces", "Rejestracja udana. Możesz się teraz zalogować.")
        else:
            self.view.display_message("Błąd", "Użytkownik o takim loginie już istnieje.")

    def handle_logout(self):
        self.model.zalogowany_uzytkownik = None
        self.view.display_message("Wylogowano", "Zostałeś wylogowany.")
        self.view.show_welcome_screen()

    def show_transactions(self):
        self.view.show_transactions()

    def show_summaries(self):
        self.view.show_summaries()

    def show_limits(self):
        self.view.show_limits()

    def show_import_export(self):
        self.view.show_import_export()

    def add_transaction(self, transakcja_data: Dict):
        if transakcja_data['typ'] == 'wydatek':
            if not self.model.sprawdz_limit(transakcja_data['kategoria'], transakcja_data['kwota']):
                result = messagebox.askyesno("Przekroczenie limitu", "Przekroczono limit budżetowy dla tej kategorii! Czy chcesz mimo to dodać transakcję?")
                if not result:
                    self.view.display_message("Anulowano", "Transakcja nie została dodana.")
                    return
        nowa_transakcja = Transakcja(**transakcja_data)
        self.model.dodaj_transakcje(nowa_transakcja)
        self.view.display_message("Sukces", "Transakcja dodana.")
        self.refresh_transactions_view()

    def edit_transaction(self, indeks: int, nowa_transakcja_data: Dict):
        transakcja_stara = self.model.transakcje[indeks]
        if transakcja_stara.typ.lower() == 'wydatek':
            # Przed edycją musimy sprawdzić limity, uwzględniając zmianę
            wydatki_przed = self.model.wydatki_kategorie.get(nowa_transakcja_data['kategoria'], 0) - transakcja_stara.kwota
            if wydatki_przed < 0:
                wydatki_przed = 0
            if not self.model.sprawdz_limit(nowa_transakcja_data['kategoria'], nowa_transakcja_data['kwota'] + wydatki_przed):
                result = messagebox.askyesno("Przekroczenie limitu", "Przekroczono limit budżetowy dla tej kategorii! Czy chcesz mimo to zaktualizować transakcję?")
                if not result:
                    self.view.display_message("Anulowano", "Transakcja nie została zaktualizowana.")
                    return
        nowa_transakcja = Transakcja(**nowa_transakcja_data)
        self.model.edytuj_transakcje(indeks, nowa_transakcja)
        self.view.display_message("Sukces", "Transakcja zaktualizowana.")
        self.refresh_transactions_view()

    def delete_transaction(self, indeks: int):
        if self.model.usun_transakcje(indeks):
            self.view.display_message("Sukces", "Transakcja usunięta.")
            self.refresh_transactions_view()
        else:
            self.view.display_message("Błąd", "Nie udało się usunąć transakcji.")

    def refresh_transactions_view(self):
        self.view.refresh_transactions_view()

    def refresh_limits_view(self):
        self.view.refresh_limits_view()

    def set_limit(self, kategoria: str, limit: float):
        self.model.ustaw_limit(kategoria, limit)
        self.view.display_message("Sukces", f"Ustawiono limit dla kategorii '{kategoria}': {limit} zł.")
        self.refresh_limits_view()

    def delete_limit(self, kategoria: str):
        if self.model.usun_limit(kategoria):
            self.view.display_message("Sukces", f"Limit dla kategorii '{kategoria}' został usunięty.")
            self.refresh_limits_view()
        else:
            self.view.display_message("Błąd", f"Limit dla kategorii '{kategoria}' nie istnieje.")

    def export_transactions(self):
        self.model.eksportuj_do_csv()
        self.view.display_message("Eksport", "Transakcje zostały wyeksportowane do pliku CSV.")

    def import_transactions(self):
        success = self.model.importuj_z_csv()
        if success:
            self.view.display_message("Import", "Transakcje zostały zaimportowane z pliku CSV.")
            self.refresh_transactions_view()
        else:
            self.view.display_message("Błąd", "Nie udało się zaimportować transakcji z pliku 'transakcje.csv'.")

    def show_add_transaction(self):
        self.view.show_add_transaction()

    def edit_selected_transaction(self):
        self.view.edit_selected_transaction()

    def delete_selected_transaction(self):
        self.view.delete_selected_transaction()

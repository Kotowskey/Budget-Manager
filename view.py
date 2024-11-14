# view.py
from colorama import init, Fore, Style
import sys

# Inicjalizacja colorama
init(autoreset=True)

class BudzetView:
    def wyswietl_menu(self):
        print(Fore.CYAN + Style.BRIGHT + "\n=== Budżet Aplikacja ===")
        print(Fore.YELLOW + "1. " + Fore.WHITE + "Dodaj transakcję")
        print(Fore.YELLOW + "2. " + Fore.WHITE + "Edytuj transakcję")
        print(Fore.YELLOW + "3. " + Fore.WHITE + "Usuń transakcję")
        print(Fore.YELLOW + "4. " + Fore.WHITE + "Wyświetl transakcje")
        print(Fore.YELLOW + "5. " + Fore.WHITE + "Wyświetl podsumowanie")
        print(Fore.YELLOW + "6. " + Fore.WHITE + "Eksportuj transakcje do CSV")
        print(Fore.YELLOW + "7. " + Fore.WHITE + "Filtruj transakcje według daty")
        print(Fore.YELLOW + "8. " + Fore.WHITE + "Ustaw limit budżetowy")
        print(Fore.YELLOW + "9. " + Fore.WHITE + "Wyjście")
        print(Fore.CYAN + "="*25)

    def pobierz_opcje(self):
        opcja = input(Fore.GREEN + "\nWybierz opcję: " + Style.RESET_ALL)
        return opcja

    def pobierz_dane_transakcji(self, edycja=False):
        if not edycja:
            typ = input(Fore.GREEN + "Typ (przychód/wydatek): " + Style.RESET_ALL)
        else:
            typ = None  # Typ nie jest edytowany
        while True:
            try:
                kwota = float(input(Fore.GREEN + "Kwota: " + Style.RESET_ALL))
                break
            except ValueError:
                self.wyswietl_komunikat(Fore.RED + "Proszę wprowadzić prawidłową kwotę." + Style.RESET_ALL)
        kategoria = input(Fore.GREEN + "Kategoria: " + Style.RESET_ALL)
        opis = input(Fore.GREEN + "Opis (opcjonalnie): " + Style.RESET_ALL)
        data = input(Fore.GREEN + "Data (YYYY-MM-DD) [opcjonalnie]: " + Style.RESET_ALL)
        return {
            'kwota': kwota,
            'kategoria': kategoria,
            'typ': typ if typ else 'przychód',
            'opis': opis,
            'data': data
        }

    def wyswietl_transakcje(self, transakcje):
        if not transakcje:
            print(Fore.RED + "\nBrak transakcji do wyświetlenia." + Style.RESET_ALL)
            return
        print(Fore.CYAN + "\n=== Transakcje ===" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"{'Nr':<5}{'Data':<12}{'Typ':<10}{'Kwota':<10}{'Kategoria':<15}{'Opis'}" + Style.RESET_ALL)
        print(Fore.CYAN + "-"*60 + Style.RESET_ALL)
        for i, t in enumerate(transakcje):
            typ_kolor = Fore.GREEN if t.typ.lower() == 'przychód' else Fore.RED
            print(f"{i:<5}{t.data:<12}{typ_kolor}{t.typ.capitalize():<10}{t.kwota:<10.2f}{Fore.WHITE}{t.kategoria:<15}{t.opis}")
        print(Fore.CYAN + "-"*60 + Style.RESET_ALL)

    def wyswietl_podsumowanie(self, saldo):
        saldo_kolor = Fore.GREEN if saldo >= 0 else Fore.RED
        print(Fore.CYAN + "\n=== Podsumowanie ===" + Style.RESET_ALL)
        print(f"Aktualne saldo: {saldo_kolor}{saldo:.2f} zł" + Style.RESET_ALL)

    def pobierz_indeks_transakcji(self):
        while True:
            try:
                indeks = int(input(Fore.GREEN + "Podaj numer transakcji: " + Style.RESET_ALL))
                return indeks
            except ValueError:
                self.wyswietl_komunikat(Fore.RED + "Proszę wprowadzić prawidłowy numer." + Style.RESET_ALL)

    def wyswietl_komunikat(self, komunikat):
        print(komunikat)

    def pobierz_limit(self):
        kategoria = input(Fore.GREEN + "Podaj kategorię: " + Style.RESET_ALL)
        while True:
            try:
                limit = float(input(Fore.GREEN + "Podaj limit miesięczny: " + Style.RESET_ALL))
                return kategoria, limit
            except ValueError:
                self.wyswietl_komunikat(Fore.RED + "Proszę wprowadzić prawidłową kwotę." + Style.RESET_ALL)

    def potwierdz_eksport(self):
        print(Fore.GREEN + "Transakcje zostały wyeksportowane do pliku 'transakcje.csv'." + Style.RESET_ALL)

    def potwierdz_ustawienie_limitu(self, kategoria, limit):
        print(Fore.GREEN + f"Ustawiono limit {limit:.2f} zł dla kategorii '{kategoria}'." + Style.RESET_ALL)

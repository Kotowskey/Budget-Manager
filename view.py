class BudzetView:
    def wyswietl_menu(self):
        print("\nMenu:")
        print("1. Dodaj transakcję")
        print("2. Edytuj transakcję")
        print("3. Usuń transakcję")
        print("4. Wyświetl transakcje")
        print("5. Wyświetl podsumowanie")
        print("6. Eksportuj transakcje do CSV")
        print("7. Filtruj transakcje według daty")
        print("8. Ustaw limit budżetowy")
        print("9. Wyjście")

    def pobierz_opcje(self):
        return input("Wybierz opcję: ")

    def pobierz_dane_transakcji(self, edycja=False):
        if not edycja:
            typ = input("Typ (przychód/wydatek): ")
        else:
            typ = None  # Typ nie jest edytowany
        kwota = float(input("Kwota: "))
        kategoria = input("Kategoria: ")
        opis = input("Opis (opcjonalnie): ")
        data = input("Data (YYYY-MM-DD) [opcjonalnie]: ")
        return {
            'kwota': kwota,
            'kategoria': kategoria,
            'typ': typ if typ else 'przychód',
            'opis': opis,
            'data': data
        }

    def wyswietl_transakcje(self, transakcje):
        print("\nTransakcje:")
        for i, t in enumerate(transakcje):
            print(f"{i}. {t.data} | {t.typ.capitalize()} | {t.kwota:.2f} | {t.kategoria} | {t.opis}")

    def wyswietl_podsumowanie(self, saldo):
        print(f"Aktualne saldo: {saldo:.2f} zł")

    def pobierz_indeks_transakcji(self):
        return int(input("Podaj numer transakcji: "))

    def wyswietl_komunikat(self, komunikat):
        print(komunikat)

    def pobierz_limit(self):
        kategoria = input("Podaj kategorię: ")
        limit = float(input("Podaj limit miesięczny: "))
        return kategoria, limit

    def potwierdz_eksport(self):
        print("Transakcje zostały wyeksportowane do pliku 'transakcje.csv'.")

    def potwierdz_ustawienie_limitu(self, kategoria, limit):
        print(f"Ustawiono limit {limit:.2f} zł dla kategorii '{kategoria}'.")

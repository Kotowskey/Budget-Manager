import unittest
import os
from model import BudzetModel, Transakcja
from datetime import datetime

class TestBudzetModel(unittest.TestCase):
    def setUp(self):
        # Inicjalizacja modelu przed każdym testem
        self.model = BudzetModel()
        # Tworzymy tymczasowego użytkownika do testów
        self.test_login = 'testuser'
        self.test_haslo = 'password'
        # Usuwamy pliki danych, jeśli istnieją, aby zapewnić czyste środowisko
        self.user_data_file = f'dane_{self.test_login}.json'
        self.user_limity_file = f'limity_{self.test_login}.json'
        if os.path.exists(self.user_data_file):
            os.remove(self.user_data_file)
        if os.path.exists(self.user_limity_file):
            os.remove(self.user_limity_file)
        # Rejestrujemy i logujemy użytkownika
        self.model.zarejestruj(self.test_login, self.test_haslo)
        self.model.zaloguj(self.test_login, self.test_haslo)

    def tearDown(self):
        # Czyszczenie po każdym teście
        if os.path.exists(self.user_data_file):
            os.remove(self.user_data_file)
        if os.path.exists(self.user_limity_file):
            os.remove(self.user_limity_file)
        if os.path.exists(self.model.uzytkownicy_plik):
            os.remove(self.model.uzytkownicy_plik)

    def test_zaloguj_poprawne_dane(self):
        wynik = self.model.zaloguj(self.test_login, self.test_haslo)
        self.assertTrue(wynik)
        self.assertEqual(self.model.zalogowany_uzytkownik, self.test_login)

    def test_zaloguj_niepoprawne_dane(self):
        wynik = self.model.zaloguj(self.test_login, 'zlehaslo')
        self.assertFalse(wynik)
        self.assertIsNone(self.model.zalogowany_uzytkownik)

    def test_zarejestruj_nowy_uzytkownik(self):
        nowy_login = 'nowyuzytkownik'
        wynik = self.model.zarejestruj(nowy_login, 'nowehaslo')
        self.assertTrue(wynik)
        self.assertIn(nowy_login, self.model.uzytkownicy)

    def test_zarejestruj_istniejacy_uzytkownik(self):
        wynik = self.model.zarejestruj(self.test_login, self.test_haslo)
        self.assertFalse(wynik)

    def test_dodaj_transakcje_przychod(self):
        transakcja = Transakcja(kwota=200.0, kategoria='Wynagrodzenie', typ='przychód')
        self.model.dodaj_transakcje(transakcja)
        self.assertIn(transakcja, self.model.transakcje)
        self.assertEqual(self.model.przychody_kategorie['Wynagrodzenie'], 200.0)

    def test_dodaj_transakcje_wydatek(self):
        transakcja = Transakcja(kwota=50.0, kategoria='Zakupy', typ='wydatek')
        self.model.dodaj_transakcje(transakcja)
        self.assertIn(transakcja, self.model.transakcje)
        self.assertEqual(self.model.wydatki_kategorie['Zakupy'], 50.0)

    def test_usun_transakcje_poprawny_indeks(self):
        transakcja = Transakcja(kwota=70.0, kategoria='Rozrywka', typ='wydatek')
        self.model.dodaj_transakcje(transakcja)
        wynik = self.model.usun_transakcje(0)
        self.assertTrue(wynik)
        self.assertNotIn(transakcja, self.model.transakcje)
        self.assertNotIn('Rozrywka', self.model.wydatki_kategorie)

    def test_usun_transakcje_niepoprawny_indeks(self):
        wynik = self.model.usun_transakcje(5)
        self.assertFalse(wynik)

    def test_edytuj_transakcje_poprawny_indeks(self):
        stara_transakcja = Transakcja(kwota=80.0, kategoria='Transport', typ='wydatek')
        nowa_transakcja = Transakcja(kwota=60.0, kategoria='Transport', typ='wydatek')
        self.model.dodaj_transakcje(stara_transakcja)
        wynik = self.model.edytuj_transakcje(0, nowa_transakcja)
        self.assertTrue(wynik)
        self.assertEqual(self.model.transakcje[0], nowa_transakcja)
        self.assertEqual(self.model.wydatki_kategorie['Transport'], 60.0)

    def test_edytuj_transakcje_niepoprawny_indeks(self):
        nowa_transakcja = Transakcja(kwota=100.0, kategoria='Inwestycje', typ='przychód')
        wynik = self.model.edytuj_transakcje(10, nowa_transakcja)
        self.assertFalse(wynik)

    def test_oblicz_saldo(self):
        self.model.dodaj_transakcje(Transakcja(kwota=500.0, kategoria='Wynagrodzenie', typ='przychód'))
        self.model.dodaj_transakcje(Transakcja(kwota=150.0, kategoria='Jedzenie', typ='wydatek'))
        saldo = self.model.oblicz_saldo()
        self.assertEqual(saldo, 350.0)

    def test_filtruj_transakcje_po_dacie(self):
        transakcja1 = Transakcja(kwota=200.0, kategoria='Wynagrodzenie', typ='przychód', data='2023-01-15')
        transakcja2 = Transakcja(kwota=50.0, kategoria='Kino', typ='wydatek', data='2023-02-20')
        self.model.transakcje.extend([transakcja1, transakcja2])
        wynik = self.model.filtruj_transakcje_po_dacie('2023-01-01', '2023-01-31')
        self.assertIn(transakcja1, wynik)
        self.assertNotIn(transakcja2, wynik)

    def test_ustaw_i_pobierz_limit(self):
        self.model.ustaw_limit('Jedzenie', 300.0)
        limit = self.model.pobierz_limit('Jedzenie')
        self.assertEqual(limit, 300.0)

    def test_sprawdz_limit_nieprzekroczony(self):
        self.model.ustaw_limit('Zakupy', 400.0)
        wynik = self.model.sprawdz_limit('Zakupy', 100.0)
        self.assertTrue(wynik)

    def test_sprawdz_limit_przekroczony(self):
        self.model.ustaw_limit('Zakupy', 200.0)
        self.model.dodaj_transakcje(Transakcja(kwota=150.0, kategoria='Zakupy', typ='wydatek'))
        wynik = self.model.sprawdz_limit('Zakupy', 100.0)
        self.assertFalse(wynik)

    def test_generuj_raport_wydatkow(self):
        self.model.dodaj_transakcje(Transakcja(kwota=50.0, kategoria='Książki', typ='wydatek'))
        self.model.dodaj_transakcje(Transakcja(kwota=70.0, kategoria='Książki', typ='wydatek'))
        raport = self.model.generuj_raport_wydatkow()
        self.assertEqual(raport['Książki'], 120.0)

    def test_generuj_raport_przychodow(self):
        self.model.dodaj_transakcje(Transakcja(kwota=1000.0, kategoria='Wynagrodzenie', typ='przychód'))
        self.model.dodaj_transakcje(Transakcja(kwota=200.0, kategoria='Bonus', typ='przychód'))
        raport = self.model.generuj_raport_przychodow()
        self.assertEqual(raport['Wynagrodzenie'], 1000.0)
        self.assertEqual(raport['Bonus'], 200.0)

    def test_eksport_i_import_csv(self):
        transakcja = Transakcja(kwota=150.0, kategoria='Elektronika', typ='wydatek')
        self.model.dodaj_transakcje(transakcja)
        self.model.eksportuj_do_csv('test_transakcje.csv')
        # Usuwamy transakcje z modelu i importujemy z CSV
        self.model.transakcje = []
        self.model.importuj_z_csv('test_transakcje.csv')
        self.assertEqual(len(self.model.transakcje), 1)
        self.assertEqual(self.model.transakcje[0].kwota, 150.0)
        os.remove('test_transakcje.csv')

    def test_usun_limit_istniejacy(self):
        self.model.ustaw_limit('Podróże', 1000.0)
        wynik = self.model.usun_limit('Podróże')
        self.assertTrue(wynik)
        self.assertNotIn('Podróże', self.model.limity)

    def test_usun_limit_nieistniejacy(self):
        wynik = self.model.usun_limit('Edukacja')
        self.assertFalse(wynik)

if __name__ == '__main__':
    unittest.main()

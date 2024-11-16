# test_model.py
import unittest
from model import BudzetModel, Transakcja

class TestBudzetModel(unittest.TestCase):
    def setUp(self):
        # Inicjalizacja modelu z pustą listą transakcji i limitów
        self.model = BudzetModel()
        self.model.transakcje = []
        self.model.limity = {}
        self.model.wydatki_kategorie = {}

    def test_dodaj_transakcje_przychod(self):
        transakcja = Transakcja(kwota=1000.0, kategoria='Pensja', typ='przychód')
        self.model.dodaj_transakcje(transakcja)
        self.assertIn(transakcja, self.model.transakcje)
        self.assertEqual(self.model.oblicz_saldo(), 1000.0)

    def test_dodaj_transakcje_wydatek(self):
        self.model.ustaw_limit('Jedzenie', 500.0)
        transakcja = Transakcja(kwota=200.0, kategoria='Jedzenie', typ='wydatek')
        self.model.dodaj_transakcje(transakcja)
        self.assertIn(transakcja, self.model.transakcje)
        self.assertEqual(self.model.oblicz_saldo(), -200.0)
        self.assertTrue(self.model.sprawdz_limit('Jedzenie'))

    def test_sprawdz_limit_przekroczony(self):
        self.model.ustaw_limit('Transport', 300.0)
        transakcja1 = Transakcja(kwota=200.0, kategoria='Transport', typ='wydatek')
        transakcja2 = Transakcja(kwota=150.0, kategoria='Transport', typ='wydatek')
        self.model.dodaj_transakcje(transakcja1)
        self.model.dodaj_transakcje(transakcja2)
        self.assertFalse(self.model.sprawdz_limit('Transport'))

    def test_usun_transakcje(self):
        transakcja = Transakcja(kwota=100.0, kategoria='Rozrywka', typ='wydatek')
        self.model.dodaj_transakcje(transakcja)
        usuniete = self.model.usun_transakcje(0)
        self.assertTrue(usuniete)
        self.assertNotIn(transakcja, self.model.transakcje)
        self.assertEqual(self.model.oblicz_saldo(), 0.0)

    def test_edytuj_transakcje(self):
        transakcja = Transakcja(kwota=100.0, kategoria='Rozrywka', typ='wydatek')
        self.model.dodaj_transakcje(transakcja)
        transakcja_edycja = Transakcja(kwota=150.0, kategoria='Rozrywka', typ='wydatek')
        edytowane = self.model.edytuj_transakcje(0, transakcja_edycja)
        self.assertTrue(edytowane)
        self.assertEqual(self.model.transakcje[0].kwota, 150.0)
        self.assertEqual(self.model.oblicz_saldo(), -150.0)

    def test_filtruj_transakcje_po_dacie(self):
        transakcja1 = Transakcja(kwota=100.0, kategoria='Transport', typ='wydatek', data='2024-01-15')
        transakcja2 = Transakcja(kwota=200.0, kategoria='Jedzenie', typ='wydatek', data='2024-02-20')
        transakcja3 = Transakcja(kwota=300.0, kategoria='Pensja', typ='przychód', data='2024-03-10')
        self.model.dodaj_transakcje(transakcja1)
        self.model.dodaj_transakcje(transakcja2)
        self.model.dodaj_transakcje(transakcja3)
        filtrowane = self.model.filtruj_transakcje_po_dacie('2024-02-01', '2024-03-01')
        self.assertIn(transakcja2, filtrowane)
        self.assertNotIn(transakcja1, filtrowane)
        self.assertNotIn(transakcja3, filtrowane)

    def test_generuj_raport_wydatkow(self):
        transakcja1 = Transakcja(kwota=100.0, kategoria='Transport', typ='wydatek')
        transakcja2 = Transakcja(kwota=200.0, kategoria='Jedzenie', typ='wydatek')
        transakcja3 = Transakcja(kwota=150.0, kategoria='Transport', typ='wydatek')
        self.model.dodaj_transakcje(transakcja1)
        self.model.dodaj_transakcje(transakcja2)
        self.model.dodaj_transakcje(transakcja3)
        raport = self.model.generuj_raport_wydatkow()
        expected = {'Transport': 250.0, 'Jedzenie': 200.0}
        self.assertEqual(raport, expected)

if __name__ == '__main__':
    unittest.main()

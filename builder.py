from datetime import datetime
from model import Transakcja

class TransakcjaBuilder:
    """
    Wzorzec projektowy BUILDER służący do tworzenia obiektu Transakcja.
    """
    def __init__(self):
        self._kwota = 0.0
        self._kategoria = ""
        self._typ = "wydatek"
        self._opis = ""
        self._data = datetime.now().strftime('%Y-%m-%d')

    def set_kwota(self, kwota: float):
        self._kwota = kwota
        return self

    def set_kategoria(self, kategoria: str):
        self._kategoria = kategoria
        return self

    def set_typ(self, typ: str):
        self._typ = typ
        return self

    def set_opis(self, opis: str):
        self._opis = opis
        return self

    def set_data(self, data: str):
        self._data = data
        return self

    def build(self) -> Transakcja:
        return Transakcja(
            kwota=self._kwota,
            kategoria=self._kategoria,
            typ=self._typ,
            opis=self._opis,
            data=self._data
        )

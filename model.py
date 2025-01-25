import os
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime

##########################################
# Wzorzec projektowy: OBSERVER (Obserwator)
##########################################

# Kod przeniesiony do pliku observer.py

##########################################
# Dane (Model) + proste klasy / dataclass
##########################################

@dataclass
class Transakcja:
    kwota: float
    kategoria: str
    typ: str
    opis: str = ""
    data: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class BudzetModel:
    transakcje: List[Transakcja] = field(default_factory=list)
    limity: Dict[str, float] = field(default_factory=dict)
    wydatki_kategorie: Dict[str, float] = field(default_factory=dict)
    przychody_kategorie: Dict[str, float] = field(default_factory=dict)
    zalogowany_uzytkownik: Optional[str] = None
    uzytkownicy: Dict[str, str] = field(default_factory=dict)
    cel_oszczedzania: Optional[object] = None  # Wskazanie na obiekt typu Cel (z observer.py)

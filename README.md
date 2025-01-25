## Budget Manager - Dokumentacja oraz instrukcja obsługi
![image](https://github.com/user-attachments/assets/a9bedf50-8662-4cc6-9d46-adfced4ab405)

### Autorzy:
- Łukasz Kotowski
- Jakub Kazimiruk
- Norbert Kopeć
- Bartłomiej Karanowski

Studia dzienne  
Kierunek: Informatyka  
Semestr: V  
Grupa zajęciowa: PS3

Data wykonania ćwiczenia:  
Listopad -- grudzień 2024 r.  
Styczeń 2025 r.

## Spis treści
- [Diagram klas budujących](#diagram-klas-budujących)
- [Opisy wzorców](#opisy-wzorców)
  - [Wzorzec MVC (Model-View-Controller)](#wzorzec-mvc-model-view-controller)
  - [Wzorzec Obserwator (Observer)](#wzorzec-obserwator-observer)
  - [Wzorzec Adapter](#wzorzec-adapter)
- [Opisy rozwiązań](#opisy-rozwiązań)
- [Podział pracy](#podział-pracy)
- [Instrukcja użytkownika](#instrukcja-użytkownika)
- [Instrukcja instalacji](#instrukcja-instalacji)

## Diagram klas budujących
```mermaid
classDiagram
    %% MVC Pattern
    class BudzetController {
        -model: BudzetModel
        -service: BudzetService
        -view: BudzetCursesView
        +uruchom()
        +logowanie()
        +obsluz_podmenu_transakcje()
        +obsluz_podmenu_podsumowania()
    }
    class BudzetModel {
        +transakcje: List[Transakcja]
        +limity: Dict[str, float]
        +wydatki_kategorie: Dict[str, float]
        +przychody_kategorie: Dict[str, float]
        +zalogowany_uzytkownik: str
        +cel_oszczedzania: Cel
    }
    class BudzetCursesView {
        +stdscr
        +wyswietl_ekran_powitalny()
        +wyswietl_glowne_menu_kategorii()
        +wyswietl_podmenu_transakcje()
        +pobierz_dane_transakcji()
    }
    class BudzetService {
        -model: BudzetModel
        +dodaj_transakcje()
        +edytuj_transakcje()
        +usun_transakcje()
        +importuj_z_csv()
        +eksportuj_do_csv()
    }
    BudzetController o-- BudzetModel
    BudzetController o-- BudzetCursesView
    BudzetController o-- BudzetService
    BudzetService o-- BudzetModel

    %% Builder Pattern
    class TransakcjaBuilder {
        -_kwota: float
        -_kategoria: str
        -_typ: str
        -_opis: str
        -_data: str
        +set_kwota(kwota: float)
        +set_kategoria(kategoria: str)
        +set_typ(typ: str)
        +set_opis(opis: str)
        +set_data(data: str)
        +build() Transakcja
    }
    class Transakcja {
        +kwota: float
        +kategoria: str
        +typ: str
        +opis: str
        +data: str
        +to_dict() Dict
    }
    TransakcjaBuilder ..> Transakcja : creates
    BudzetModel o-- Transakcja

    %% Observer Pattern
    class Obserwator {
        <<interface>>
        +aktualizuj(podmiot: Podmiot)*
    }
    class Podmiot {
        -obserwatorzy: List[Obserwator]
        +dodaj(obserwator: Obserwator)
        +usun(obserwator: Obserwator)
        +powiadomObserwatorow()
    }
    class Dochod {
        -ostatnia_kwota: float
        +dodajDochod(kwota: float)
    }
    class Wydatek {
        -ostatnia_kwota: float
        +dodajWydatek(kwota: float)
    }
    class Cel {
        -cel_oszczednosci: float
        -obecneOszczednosci: float
        -uzytkownik: str
        +aktualizuj(podmiot: Podmiot)
        +monitorujPostep()
        +ustaw_nowy_cel(nowy_cel: float)
    }
    Podmiot <|-- Dochod
    Podmiot <|-- Wydatek
    Obserwator <|.. Cel
    Podmiot o-- Obserwator
    BudzetService o-- Dochod
    BudzetService o-- Wydatek
    BudzetModel o-- Cel

    %% Adapter Pattern
    class IExporter {
        <<interface>>
        +eksportuj(dane: List[Dict], nazwa_pliku: str)*
    }
    class CsvExporter {
        +export_to_csv(dane: List[Dict], nazwa_pliku: str)
    }
    class JsonExporter {
        +export_to_json(dane: List[Dict], nazwa_pliku: str)
    }
    class EksporterCSV {
        -_csv_exporter: CsvExporter
        +eksportuj(dane: List[Dict], nazwa_pliku: str)
    }
    class EksporterJSON {
        -_json_exporter: JsonExporter
        +eksportuj(dane: List[Dict], nazwa_pliku: str)
    }
    IExporter <|.. EksporterCSV
    IExporter <|.. EksporterJSON
    EksporterCSV o-- CsvExporter
    EksporterJSON o-- JsonExporter
    BudzetService ..> IExporter : uses

    %% Factory Pattern
    class Wykres {
        <<abstract>>
        +rysuj(raport: Dict[str, float], view: BudzetCursesView)*
    }
    class WykresWydatkow {
        +rysuj(raport: Dict[str, float], view: BudzetCursesView)
    }
    class WykresPrzychodow {
        +rysuj(raport: Dict[str, float], view: BudzetCursesView)
    }
    class FabrykaWykresow {
        +utworz_wykres(typ: str) Wykres$
    }
    Wykres <|-- WykresWydatkow
    Wykres <|-- WykresPrzychodow
    FabrykaWykresow ..> Wykres : creates
    BudzetController ..> FabrykaWykresow : uses
```

## Opisy wzorców

### Wzorzec MVC (Model-View-Controller)

**Cel użycia:**
- Umożliwienie niezależnego rozwoju i testowania komponentów
- Separacja logiki biznesowej od prezentacji danych
- Ułatwienie utrzymania i modyfikacji kodu poprzez jasny podział odpowiedzialności

**Przyporządkowanie klas:**
- Model (BudzetModel)
- View (BudzetCursesView)
- Controller

**Interakcje między komponentami:**
1. **Przepływ danych:**
   - Controller pobiera dane od View
   - Controller aktualizuje Model poprzez Service
   - View wyświetla dane z Modelu otrzymane przez Controller

2. **Separacja odpowiedzialności:**
   - Model: przechowywanie danych i stan aplikacji
   - View: interfejs użytkownika i prezentacja danych
   - Controller: logika aplikacji i koordynacja

### Wzorzec Obserwator (Observer)

**Cel użycia:**
- Elastyczne dodawanie nowych reakcji na zmiany
- Automatyczne powiadamianie o zmianach w stanie aplikacji
- Luźne powiązanie między komponentami systemu

### Wzorzec Adapter

**Cel użycia:**  
Wzorzec Adapter został wykorzystany do ujednolicenia interfejsu eksportu danych dla różnych formatów (CSV, JSON). Umożliwia on łatwe dodawanie kolejnych formatów eksportu, spójną komunikację między modelem i różnymi formatami zapisu danych.

**Przyporządkowanie klas:**
- Target (Cel) - UniwersalnyInterfejsEksportu
- Adapter - AdapterEksportu, AdapterEksportuCSV, AdapterEksportuJSON
- Adaptee (Adaptowany) - EksporterCSV, EksporterJSON
- Client (Klient) - EksportDanych

## Opisy rozwiązań

**Język programowania:** Python

**Biblioteki standardowe:**
- **json**: Serializacja i deserializacja danych w formacie JSON
- **os**: Operacje na systemie plików
- **datetime**: Obsługa dat i czasu
- **csv**: Import i eksport danych w formacie CSV
- **logging**: Tworzenie logów aplikacji

**Biblioteki zewnętrzne:**
- **curses**: Tworzenie interfejsu tekstowego (TUI)

**Specyficzne rozwiązania Pythona:**
- Dekoratory (@dataclass)
- Type hinting
- List comprehensions
- Słowniki
- Context managers

## Podział pracy

### Łukasz Kotowski
- Wzorzec MVC
- Wzorzec Observator
- Diagramy UML
- Interfejs tekstowy windows-curses
- Interfejs graficzny custom-tkinter
- Dokumentacja

### Jakub Kazimiruk
- Wzorzec Adapter
- Dokumentacja
- Interfejs tekstowy windows-curses (Importowanie i eksportowanie)

### Norbert Kopeć
- Wzorzec Fabryka

### Bartłomiej Karanowski
- Wzorzec Budowniczy
- Dokumentacja

## Instrukcja instalacji

### Wymagania
- Python
- Custom Tkinter (do obsługi interfejsu graficznego)
- Curses (do obsługi interfejsu tekstowego)
- Matplotlib

### Instalacja komponentów
```bash
pip install customtkinter
pip install windows-curses
pip install matplotlib
```

### Uruchomienie aplikacji
1. Przejdź do folderu programu
2. Uruchom program komendą:
```bash
python main.py
```

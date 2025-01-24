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
    }

    class BudzetModel {
        +transakcje: List[Transakcja]
        +limity: Dict[str, float]
        +wydatki_kategorie: Dict[str, float]
        +przychody_kategorie: Dict[str, float]
        +zalogowany_uzytkownik: str
        +cel_oszczedzania: Cel
        +uzytkownicy: Dict[str, str]
    }

    class BudzetCursesView {
        +stdscr: curses.window
        +wyswietl_menu()
        +pobierz_input()
        +wyswietl_transakcje()
        +wyswietl_raport_wydatkow()
        +wyswietl_raport_przychodow()
    }

    %% Builder Pattern
    class TransakcjaBuilder {
        -_kwota: float
        -_kategoria: str
        -_typ: str
        -_opis: str
        -_data: str
        +set_kwota()
        +set_kategoria()
        +build()
    }

    class Transakcja {
        +kwota: float
        +kategoria: str
        +typ: str
        +opis: str
        +data: str
        +to_dict()
    }

    %% Observer Pattern
    class Podmiot {
        +obserwatorzy: List[Obserwator]
        +dodaj()
        +usun()
        +powiadomObserwatorow()
    }

    class Obserwator {
        <<interface>>
        +aktualizuj()*
    }

    class Dochod {
        +ostatnia_kwota: float
        +dodajDochod()
    }

    class Wydatek {
        +ostatnia_kwota: float
        +dodajWydatek()
    }

    class Cel {
        +cel_oszczednosci: float
        +obecneOszczednosci: float
        +aktualizuj()
        +monitorujPostep()
        +zapisz_cel()
        +wczytaj_cel()
    }

    %% Factory & Template Method Pattern
    class Wykres {
        <<abstract>>
        +rysuj()*
    }

    class WykresWydatkow {
        +rysuj()
    }

    class WykresPrzychodow {
        +rysuj()
    }

    class FabrykaWykresow {
        +utworz_wykres()
    }

    %% Adapter Pattern
    class EksporterCSV {
        +eksportujDoCSV()
    }

    class EksporterJSON {
        +eksportujDoJSON()
    }

    class BudzetService {
        -model: BudzetModel
        -dochod: Dochod
        -wydatek: Wydatek
        -data_dir: str
        -users_dir: str
        -exports_dir: str
        +dodaj_transakcje()
        +edytuj_transakcje()
        +usun_transakcje()
        +zaloguj()
        +zarejestruj()
        +eksportuj_do_csv()
        +eksportuj_do_json()
    }

    %% MVC Pattern Relationships
    BudzetController --> BudzetModel
    BudzetController --> BudzetService
    BudzetController --> BudzetCursesView
    BudzetService --> BudzetModel

    %% Builder Pattern Relationship
    TransakcjaBuilder --> Transakcja
    BudzetService ..> TransakcjaBuilder

    %% Observer Pattern Relationships
    Dochod --|> Podmiot
    Wydatek --|> Podmiot
    Cel ..|> Obserwator
    Podmiot --> Obserwator
    BudzetService --> Dochod
    BudzetService --> Wydatek

    %% Factory & Template Method Relationships
    WykresWydatkow --|> Wykres
    WykresPrzychodow --|> Wykres
    FabrykaWykresow --> Wykres
    BudzetController ..> FabrykaWykresow
    BudzetCursesView --> Wykres

    %% Adapter Pattern Relationships
    BudzetService --> EksporterCSV
    BudzetService --> EksporterJSON

    %% Model Relationships
    BudzetModel --> Transakcja
    BudzetModel --> Cel

    %% Service Layer Access
    BudzetService ..> EksporterCSV
    BudzetService ..> EksporterJSON
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

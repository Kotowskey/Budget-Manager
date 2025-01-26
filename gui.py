import customtkinter as ctk
from typing import Optional, Dict, List
import json
from datetime import datetime
from model import BudzetModel, Transakcja
from budzet_service import BudzetService
from builder import TransakcjaBuilder
from fabrica import FabrykaWykresow
from tkinter import messagebox
import os

class MenedzerBudzetuGUI:
    def __init__(self):
        self.model = BudzetModel()
        self.serwis = BudzetService(self.model)
        
        # Główne okno
        self.root = ctk.CTk()
        self.root.title("Menedżer Budżetu")
        self.root.geometry("800x600")
        
        # Konfiguracja motywu
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.biezace_okno = None
        self.pokaz_okno_logowania()

    def wyczysc_okno(self):
        if self.biezace_okno:
            self.biezace_okno.destroy()

    def pokaz_okno_logowania(self):
        self.wyczysc_okno()
        self.biezace_okno = OknoLogowania(self.root, self.obsluga_logowania, self.obsluga_rejestracji)

    def pokaz_okno_glowne(self):
        self.wyczysc_okno()
        self.biezace_okno = OknoGlowne(self.root, self.serwis, self.model, self.pokaz_okno_logowania)

    def obsluga_logowania(self, login: str, haslo: str):
        if self.serwis.zaloguj(login, haslo):
            self.pokaz_okno_glowne()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")

    def obsluga_rejestracji(self, login: str, haslo: str):
        if self.serwis.zarejestruj(login, haslo):
            messagebox.showinfo("Sukces", "Rejestracja zakończona sukcesem")
        else:
            messagebox.showerror("Błąd", "Użytkownik o takiej nazwie już istnieje")

    def uruchom(self):
        self.root.mainloop()


class OknoLogowania(ctk.CTkFrame):
    def __init__(self, master, funkcja_logowania, funkcja_rejestracji):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Formularz logowania
        ctk.CTkLabel(self, text="Menedżer Budżetu", font=("Helvetica", 24, "bold")).pack(pady=20)
        
        self.pole_uzytkownik = ctk.CTkEntry(self, placeholder_text="Nazwa użytkownika")
        self.pole_uzytkownik.pack(pady=10)
        
        self.pole_haslo = ctk.CTkEntry(self, placeholder_text="Hasło", show="*")
        self.pole_haslo.pack(pady=10)
        
        ctk.CTkButton(self, text="Zaloguj się", command=lambda: funkcja_logowania(
            self.pole_uzytkownik.get(), self.pole_haslo.get()
        )).pack(pady=10)
        
        ctk.CTkButton(self, text="Zarejestruj się", command=lambda: funkcja_rejestracji(
            self.pole_uzytkownik.get(), self.pole_haslo.get()
        )).pack(pady=10)


class OknoGlowne(ctk.CTkFrame):
    def __init__(self, master, serwis: BudzetService, model: BudzetModel, funkcja_wylogowania):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.serwis = serwis
        self.model = model
        
        # Panel boczny
        panel_boczny = ctk.CTkFrame(self, width=200)
        panel_boczny.pack(side="left", fill="y", padx=10, pady=10)
        
        przyciski = [
            ("Transakcje", self.pokaz_okno_transakcji),
            ("Podsumowanie", self.pokaz_okno_podsumowania),
            ("Limity", self.pokaz_okno_limitow),
            ("Cele", self.pokaz_okno_celow),
            ("Import/Eksport", self.pokaz_okno_import_eksport),
            ("Wyloguj się", funkcja_wylogowania)
        ]
        
        for tekst, polecenie in przyciski:
            ctk.CTkButton(panel_boczny, text=tekst, command=polecenie).pack(pady=5, padx=10, fill="x")
        
        # Główna część okna
        self.zawartosc = ctk.CTkFrame(self)
        self.zawartosc.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.pokaz_okno_transakcji()

    def wyczysc_zawartosc(self):
        for widget in self.zawartosc.winfo_children():
            widget.destroy()

    def pokaz_okno_transakcji(self):
        self.wyczysc_zawartosc()
        OknoTransakcji(self.zawartosc, self.serwis, self.model)

    def pokaz_okno_podsumowania(self):
        self.wyczysc_zawartosc()
        OknoPodsumowania(self.zawartosc, self.serwis)

    def pokaz_okno_limitow(self):
        self.wyczysc_zawartosc()
        OknoLimitow(self.zawartosc, self.serwis)

    def pokaz_okno_celow(self):
        self.wyczysc_zawartosc()
        OknoCelow(self.zawartosc, self.serwis, self.model)

    def pokaz_okno_import_eksport(self):
        self.wyczysc_zawartosc()
        OknoImportEksport(self.zawartosc, self.serwis)


class OknoTransakcji(ctk.CTkFrame):
    def __init__(self, master, serwis: BudzetService, model: BudzetModel):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.serwis = serwis
        self.model = model
        
        # Panel przycisków
        panel_przyciskow = ctk.CTkFrame(self)
        panel_przyciskow.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(panel_przyciskow, text="Dodaj transakcję", 
                      command=self.dodaj_transakcje).pack(side="left", padx=5)
        ctk.CTkButton(panel_przyciskow, text="Edytuj transakcję", 
                      command=self.edytuj_transakcje).pack(side="left", padx=5)
        ctk.CTkButton(panel_przyciskow, text="Usuń transakcję", 
                      command=self.usun_transakcje).pack(side="left", padx=5)
        
        # Lista transakcji
        self.panel_transakcji = ctk.CTkScrollableFrame(self)
        self.panel_transakcji.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.odswiez_transakcje()

    def odswiez_transakcje(self):
        for widget in self.panel_transakcji.winfo_children():
            widget.destroy()
            
        naglowki = ["Data", "Typ", "Kwota", "Kategoria", "Opis"]
        for i, naglowek in enumerate(naglowki):
            ctk.CTkLabel(self.panel_transakcji, text=naglowek, font=("Helvetica", 12, "bold")
                        ).grid(row=0, column=i, padx=5, pady=5)
            
        for i, t in enumerate(self.model.transakcje, 1):
            ctk.CTkLabel(self.panel_transakcji, text=t.data).grid(row=i, column=0, padx=5, pady=2)
            ctk.CTkLabel(self.panel_transakcji, text=t.typ).grid(row=i, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.panel_transakcji, text=f"{t.kwota:.2f}").grid(row=i, column=2, padx=5, pady=2)
            ctk.CTkLabel(self.panel_transakcji, text=t.kategoria).grid(row=i, column=3, padx=5, pady=2)
            ctk.CTkLabel(self.panel_transakcji, text=t.opis).grid(row=i, column=4, padx=5, pady=2)

    def dodaj_transakcje(self):
        dialog = DialogTransakcji(self, self.serwis)
        self.wait_window(dialog)
        self.odswiez_transakcje()

    def edytuj_transakcje(self):
        dialog = DialogWyboruTransakcji(self, self.model.transakcje, "Edytuj transakcję")
        self.wait_window(dialog)
        if dialog.wybrany_indeks is not None:
            dialog_transakcji = DialogTransakcji(
                self, self.serwis,
                self.model.transakcje[dialog.wybrany_indeks],
                dialog.wybrany_indeks
            )
            self.wait_window(dialog_transakcji)
            self.odswiez_transakcje()

    def usun_transakcje(self):
        dialog = DialogWyboruTransakcji(self, self.model.transakcje, "Usuń transakcję")
        self.wait_window(dialog)
        if dialog.wybrany_indeks is not None:
            if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę transakcję?"):
                self.serwis.usun_transakcje(dialog.wybrany_indeks)
                self.odswiez_transakcje()


class DialogTransakcji(ctk.CTkToplevel):
    def __init__(self, rodzic, serwis: BudzetService, transakcja: Optional[Transakcja] = None,
                 indeks: Optional[int] = None):
        super().__init__(rodzic)
        self.serwis = serwis
        self.transakcja = transakcja
        self.indeks = indeks
        
        self.title("Edytuj transakcję" if transakcja else "Dodaj transakcję")
        self.geometry("400x500")
        
        # Pola formularza
        ctk.CTkLabel(self, text="Typ:").pack(pady=5)
        self.typ_var = ctk.StringVar(value=transakcja.typ if transakcja else "wydatek")
        panel_typu = ctk.CTkFrame(self)
        panel_typu.pack(fill="x", padx=20)
        ctk.CTkRadioButton(panel_typu, text="Wydatek", variable=self.typ_var, 
                           value="wydatek").pack(side="left", padx=10)
        ctk.CTkRadioButton(panel_typu, text="Przychód", variable=self.typ_var, 
                           value="przychód").pack(side="left", padx=10)
        
        ctk.CTkLabel(self, text="Kwota:").pack(pady=5)
        self.pole_kwota = ctk.CTkEntry(self)
        self.pole_kwota.pack(pady=5)
        if transakcja:
            self.pole_kwota.insert(0, str(transakcja.kwota))
        
        ctk.CTkLabel(self, text="Kategoria:").pack(pady=5)
        self.pole_kategoria = ctk.CTkEntry(self)
        self.pole_kategoria.pack(pady=5)
        if transakcja:
            self.pole_kategoria.insert(0, transakcja.kategoria)
        
        ctk.CTkLabel(self, text="Opis:").pack(pady=5)
        self.pole_opis = ctk.CTkEntry(self)
        self.pole_opis.pack(pady=5)
        if transakcja:
            self.pole_opis.insert(0, transakcja.opis)
        
        ctk.CTkLabel(self, text="Data (RRRR-MM-DD):").pack(pady=5)
        self.pole_data = ctk.CTkEntry(self)
        self.pole_data.pack(pady=5)
        if transakcja:
            self.pole_data.insert(0, transakcja.data)
        else:
            self.pole_data.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        ctk.CTkButton(self, text="Zapisz", command=self.zapisz).pack(pady=20)

    def zapisz(self):
        try:
            kwota = float(self.pole_kwota.get())
            kategoria = self.pole_kategoria.get().strip()
            if not kategoria:
                raise ValueError("Kategoria nie może być pusta")
                
            nowa_transakcja = (TransakcjaBuilder()
                               .set_kwota(kwota)
                               .set_kategoria(kategoria)
                               .set_typ(self.typ_var.get())
                               .set_opis(self.pole_opis.get())
                               .set_data(self.pole_data.get())
                               .build())
            
            if self.transakcja:  # edycja istniejącej
                self.serwis.edytuj_transakcje(self.indeks, nowa_transakcja)
            else:  # nowa transakcja
                self.serwis.dodaj_transakcje(nowa_transakcja)
            
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))


class DialogWyboruTransakcji(ctk.CTkToplevel):
    def __init__(self, rodzic, transakcje: List[Transakcja], tytul: str):
        super().__init__(rodzic)
        self.title(tytul)
        self.geometry("600x400")
        self.wybrany_indeks = None
        
        # Ramka przewijalna na transakcje
        panel = ctk.CTkScrollableFrame(self)
        panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Wyświetlenie transakcji
        for i, t in enumerate(transakcje):
            tekst = f"{t.data} | {t.typ} | {t.kwota:.2f} | {t.kategoria} | {t.opis}"
            przycisk = ctk.CTkButton(
                panel, 
                text=tekst,
                command=lambda idx=i: self.wybierz_transakcje(idx)
            )
            przycisk.pack(fill="x", pady=2)

    def wybierz_transakcje(self, indeks: int):
        self.wybrany_indeks = indeks
        self.destroy()


class OknoPodsumowania(ctk.CTkFrame):
    def __init__(self, master, serwis: BudzetService):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.serwis = serwis
        
        # Saldo
        ramka_saldo = ctk.CTkFrame(self)
        ramka_saldo.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(ramka_saldo, text="Aktualne saldo:", 
                     font=("Helvetica", 16, "bold")).pack(side="left", padx=10)
        saldo = self.serwis.oblicz_saldo()
        ctk.CTkLabel(ramka_saldo, text=f"{saldo:.2f}", 
                     font=("Helvetica", 16)).pack(side="left")
        
        # Ramka z raportami (zakładki)
        ramka_raporty = ctk.CTkTabview(self)
        ramka_raporty.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Zakładka Wydatki
        zakladka_wydatki = ramka_raporty.add("Wydatki")
        self.utworz_zakladke_raportu(zakladka_wydatki, self.serwis.generuj_raport_wydatkow())
        
        # Zakładka Przychody
        zakladka_przychody = ramka_raporty.add("Przychody")
        self.utworz_zakladke_raportu(zakladka_przychody, self.serwis.generuj_raport_przychodow())

    def utworz_zakladke_raportu(self, zakladka, dane: Dict[str, float]):
        ramka = ctk.CTkScrollableFrame(zakladka)
        ramka.pack(fill="both", expand=True)
        
        suma = sum(dane.values())
        for kategoria, kwota in dane.items():
            procent = (kwota / suma * 100) if suma > 0 else 0
            wiersz = ctk.CTkFrame(ramka)
            wiersz.pack(fill="x", pady=2)
            ctk.CTkLabel(wiersz, text=kategoria).pack(side="left", padx=5)
            ctk.CTkLabel(wiersz, text=f"{kwota:.2f}").pack(side="left", padx=5)
            ctk.CTkLabel(wiersz, text=f"{procent:.1f}%").pack(side="left", padx=5)
            
            # Pasek postępu
            pasek_postepu = ctk.CTkProgressBar(wiersz)
            pasek_postepu.pack(side="left", padx=5, fill="x", expand=True)
            pasek_postepu.set(procent/100)


class OknoLimitow(ctk.CTkFrame):
    def __init__(self, master, serwis: BudzetService):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.serwis = serwis
        
        # Przyciski
        panel_przyciskow = ctk.CTkFrame(self)
        panel_przyciskow.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(panel_przyciskow, text="Ustaw limit", 
                      command=self.ustaw_limit).pack(side="left", padx=5)
        ctk.CTkButton(panel_przyciskow, text="Usuń limit", 
                      command=self.usun_limit).pack(side="left", padx=5)
        
        # Lista limitów
        self.panel_limitow = ctk.CTkScrollableFrame(self)
        self.panel_limitow.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.odswiez_limity()

    def odswiez_limity(self):
        for widget in self.panel_limitow.winfo_children():
            widget.destroy()
            
        for kategoria, limit in self.serwis.model.limity.items():
            wiersz = ctk.CTkFrame(self.panel_limitow)
            wiersz.pack(fill="x", pady=2)
            
            ctk.CTkLabel(wiersz, text=kategoria).pack(side="left", padx=5)
            ctk.CTkLabel(wiersz, text=f"{limit:.2f}").pack(side="left", padx=5)
            
            obecne = self.serwis.model.wydatki_kategorie.get(kategoria, 0)
            procent = (obecne / limit * 100) if limit > 0 else 0
            
            pasek_postepu = ctk.CTkProgressBar(wiersz)
            pasek_postepu.pack(side="left", padx=5, fill="x", expand=True)
            pasek_postepu.set(procent/100)
            
            ctk.CTkLabel(wiersz, text=f"{procent:.1f}%").pack(side="left", padx=5)

    def ustaw_limit(self):
        dialog = DialogLimitu(self, self.serwis)
        self.wait_window(dialog)
        self.odswiez_limity()

    def usun_limit(self):
        dialog = DialogWyboruKategorii(self, list(self.serwis.model.limity.keys()), 
                                       "Wybierz kategorię do usunięcia limitu")
        self.wait_window(dialog)
        if dialog.wybrana_kategoria:
            self.serwis.usun_limit(dialog.wybrana_kategoria)
            self.odswiez_limity()


class DialogLimitu(ctk.CTkToplevel):
    def __init__(self, rodzic, serwis: BudzetService):
        super().__init__(rodzic)
        self.serwis = serwis
        self.title("Ustaw limit")
        self.geometry("300x200")
        
        ctk.CTkLabel(self, text="Kategoria:").pack(pady=5)
        self.pole_kategoria = ctk.CTkEntry(self)
        self.pole_kategoria.pack(pady=5)
        
        ctk.CTkLabel(self, text="Limit:").pack(pady=5)
        self.pole_limit = ctk.CTkEntry(self)
        self.pole_limit.pack(pady=5)
        
        ctk.CTkButton(self, text="Zapisz", command=self.zapisz).pack(pady=20)

    def zapisz(self):
        try:
            kategoria = self.pole_kategoria.get().strip()
            limit = float(self.pole_limit.get())
            
            if not kategoria:
                raise ValueError("Kategoria nie może być pusta")
            if limit <= 0:
                raise ValueError("Limit musi być większy od 0")
                
            self.serwis.ustaw_limit(kategoria, limit)
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))


class DialogWyboruKategorii(ctk.CTkToplevel):
    def __init__(self, rodzic, kategorie: List[str], tytul: str):
        super().__init__(rodzic)
        self.title(tytul)
        self.geometry("300x400")
        self.wybrana_kategoria = None
        
        panel = ctk.CTkScrollableFrame(self)
        panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        for kat in kategorie:
            ctk.CTkButton(
                panel,
                text=kat,
                command=lambda k=kat: self.wybierz_kategorie(k)
            ).pack(fill="x", pady=2)

    def wybierz_kategorie(self, kategoria: str):
        self.wybrana_kategoria = kategoria
        self.destroy()


class OknoCelow(ctk.CTkFrame):
    def __init__(self, master, serwis: BudzetService, model: BudzetModel):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.serwis = serwis
        self.model = model
        
        if not self.model.cel_oszczedzania:
            ctk.CTkLabel(self, text="Brak zdefiniowanego celu oszczędzania").pack(pady=20)
            return
            
        # Informacje o aktualnym celu
        ramka_info = ctk.CTkFrame(self)
        ramka_info.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(ramka_info, text="Obecny cel:", 
                     font=("Helvetica", 16, "bold")).pack(side="left", padx=10)
        self.et_kwota_celu = ctk.CTkLabel(ramka_info, 
                                          text=f"{self.model.cel_oszczedzania.cel_oszczednosci:.2f}",
                                          font=("Helvetica", 16))
        self.et_kwota_celu.pack(side="left")
        
        # Pasek postępu
        ramka_postep = ctk.CTkFrame(self)
        ramka_postep.pack(fill="x", padx=10, pady=10)
        
        obecne = self.model.cel_oszczedzania.obecneOszczednosci
        cel = self.model.cel_oszczedzania.cel_oszczednosci
        procent = (obecne / cel * 100) if cel > 0 else 0
        
        ctk.CTkLabel(ramka_postep, text="Postęp:").pack(pady=5)
        self.pasek_celu = ctk.CTkProgressBar(ramka_postep)
        self.pasek_celu.pack(fill="x", padx=20, pady=5)
        self.pasek_celu.set(procent/100)
        
        ctk.CTkLabel(ramka_postep, text=f"{procent:.1f}%").pack(pady=5)
        
        # Przycisk do ustawiania nowego celu
        ctk.CTkButton(self, text="Ustaw nowy cel", 
                      command=self.ustaw_nowy_cel).pack(pady=20)

    def ustaw_nowy_cel(self):
        dialog = DialogCelu(self, self.model)
        self.wait_window(dialog)
        # odświeżenie po ustawieniu nowego celu
        self.__init__(self.master, self.serwis, self.model)


class DialogCelu(ctk.CTkToplevel):
    def __init__(self, rodzic, model: BudzetModel):
        super().__init__(rodzic)
        self.model = model
        self.title("Ustaw nowy cel")
        self.geometry("300x150")
        
        ctk.CTkLabel(self, text="Kwota nowego celu:").pack(pady=5)
        self.pole_kwota_celu = ctk.CTkEntry(self)
        self.pole_kwota_celu.pack(pady=5)
        
        ctk.CTkButton(self, text="Zapisz", command=self.zapisz).pack(pady=20)

    def zapisz(self):
        try:
            kwota = float(self.pole_kwota_celu.get())
            if kwota <= 0:
                raise ValueError("Cel musi być większy od 0")
            
            self.model.cel_oszczedzania.ustaw_nowy_cel(kwota)
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))


class OknoImportEksport(ctk.CTkFrame):
    def __init__(self, master, serwis: BudzetService):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.serwis = serwis
        
        # Eksport
        ramka_eksport = ctk.CTkFrame(self)
        ramka_eksport.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(ramka_eksport, text="Eksport:", 
                     font=("Helvetica", 14, "bold")).pack(pady=5)
        ctk.CTkButton(ramka_eksport, text="Eksportuj do CSV",
                      command=lambda: self.eksportuj_dane("csv")).pack(fill="x", pady=2)
        ctk.CTkButton(ramka_eksport, text="Eksportuj do JSON",
                      command=lambda: self.eksportuj_dane("json")).pack(fill="x", pady=2)
        
        # Import
        ramka_import = ctk.CTkFrame(self)
        ramka_import.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(ramka_import, text="Import:", 
                     font=("Helvetica", 14, "bold")).pack(pady=5)
        ctk.CTkButton(ramka_import, text="Importuj z CSV",
                      command=lambda: self.importuj_dane("csv")).pack(fill="x", pady=2)
        ctk.CTkButton(ramka_import, text="Importuj z JSON",
                      command=lambda: self.importuj_dane("json")).pack(fill="x", pady=2)

    def eksportuj_dane(self, typ_formatu: str):
        try:
            if typ_formatu == "csv":
                self.serwis.eksportuj_do_csv("data/exports/transakcje.csv")
            else:
                self.serwis.eksportuj_do_json("data/exports/transakcje.json")
            messagebox.showinfo("Sukces", f"Dane wyeksportowane do {typ_formatu.upper()} pomyślnie")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyeksportować danych: {str(e)}")

    def importuj_dane(self, typ_formatu: str):
        try:
            powodzenie = False
            if typ_formatu == "csv":
                powodzenie = self.serwis.importuj_z_csv("data/exports/transakcje.csv")
            else:
                powodzenie = self.serwis.importuj_z_json("data/exports/transakcje.json")
                
            if powodzenie:
                messagebox.showinfo("Sukces", f"Dane zaimportowane z {typ_formatu.upper()} pomyślnie")
            else:
                messagebox.showerror("Błąd", f"Nie udało się zaimportować danych z {typ_formatu.upper()}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zaimportować danych: {str(e)}")


if __name__ == "__main__":
    aplikacja = MenedzerBudzetuGUI()
    aplikacja.uruchom()

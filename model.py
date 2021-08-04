import json
import calendar


class CustomHTMLCal(calendar.HTMLCalendar):
    cssclasses = [style + " text-nowrap" for style in
                  calendar.HTMLCalendar.cssclasses]
    cssclass_month_head = "text-center month-head"
    cssclass_month = "month"
    cssclass_year = "year"

# MANJKA ZA BELEŽENJE V DATUM

# ========================================================================================================================

class Stanje:
    def __init__(self):
        self.spiski = []
        self.aktualni_spisek = None
    
    def dodaj_spisek(self, spisek):
        self.spiski.append(spisek)
        if not self.aktualni_spisek:
            self.aktualni_spisek = spisek
    
    def pobrisi_spisek(self, spisek):
        self.spiski.remove(spisek)
    
    def zamenjaj_spisek(self, spisek):
        self.aktualni_spisek = spisek
    
    def dodaj_opravilo(self, opravilo, spisek):
        spisek.dodaj_opravilo(opravilo)
    
    def pobrisi_opravilo(self, opravilo, spisek):
        self.aktualni_spisek.pobrisi_opravilo(opravilo)

    def v_slovar(self):
        return {
            "spiski": [spisek.v_slovar() for spisek in self.spiski],
            "aktualni_spisek": self.spiski.index(self.aktualni_spisek)
            if self.aktualni_spisek
            else None,
        }

    @staticmethod
    def iz_slovarja(slovar):
        stanje = Stanje()
        stanje.spiski = [
            Spisek.iz_slovarja(sl_spiska) for sl_spiska in slovar["spiski"]
        ]
        if slovar["aktualni_spisek"] is not None:
            stanje.aktualni_spisek = stanje.spiski[slovar["aktualni_spisek"]]
        return stanje

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return Stanje.iz_slovarja(slovar)

    def preveri_podatke_novega_spiska(self, ime):
        napake = {}
        if not ime:
            napake["ime"] = "Ime mora biti neprazno."
        for spisek in self.spiski:
            if spisek.ime == ime:
                napake["ime"] = "Ime je že zasedeno."
        return napake

# ========================================================================================================================

class Spisek:
    def __init__(self, ime):
        self.ime = ime
        self.opravila = []

    def dodaj_opravilo(self, opravilo):
        self.opravila.append(opravilo)

    def v_slovar(self):
        return {
            "ime": self.ime,
            "opravila": [opravilo.v_slovar() for opravilo in self.opravila],
        }

    @staticmethod
    def iz_slovarja(slovar):
        spisek = Spisek(slovar["ime"])
        spisek.opravila = [
            Opravilo.iz_slovarja(sl_opravila) for sl_opravila in slovar["opravila"]
        ]
        return spisek

# ========================================================================================================================

class Opravilo:
    def __init__(self, ime, opis):
        self.ime = ime
        self.opis = opis 
    
    def v_slovar(self):
        return {
            "ime": self.ime,
            "opis": self.opis,
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Opravilo(
            slovar["ime"],
            slovar["opis"],
        )

import json
import hashlib

from datetime import date
danes = date.today()
danasnji_datum = danes.strftime("%Y-%m-%d")

def zasifriraj_geslo(geslo_v_cistopisu):
    h = hashlib.blake2b()
    h.update(geslo_v_cistopisu.encode(encoding="utf-8"))
    return h.hexdigest()

# ========================================================================================================================

class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, koledar):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.koledar = koledar

    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Uporabnik.preberi_iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik        
        else:
            raise ValueError("Geslo je napačno")

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.preberi_iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            zasifrirano_geslo = zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, Koledar())
            uporabnik.shrani_v_datoteko()
            return uporabnik

    def preveri_geslo(self, geslo_v_cistopisu):
        return self.zasifrirano_geslo == zasifriraj_geslo(geslo_v_cistopisu)

    def nastavi_geslo(self, geslo_v_cistopisu):
        self.zasifrirano_geslo = zasifriraj_geslo(geslo_v_cistopisu)

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "koledar": self.koledar.v_slovar()
        }

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        koledar = Koledar.iz_slovarja(slovar["koledar"])
        return Uporabnik(uporabnisko_ime, zasifrirano_geslo, koledar)

    def shrani_v_datoteko(self):
        with open(Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    @staticmethod
    def preberi_iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as dat:
                slovar = json.load(dat)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None

# ========================================================================================================================

class Koledar:
    def __init__(self, datumi=None, aktualni_datum=None):
        if aktualni_datum == None:
            datumi = {danasnji_datum: Stanje(dnevnik="")}
            aktualni_datum = danasnji_datum
            self.datumi = datumi
            self.aktualni_datum = aktualni_datum
        self.datumi = datumi    # datumi je slovar stanj. Ključi so datumi, vrednosti so stanja ("spiski", "aktualni_spisek" in "dnevnik")
        self.aktualni_datum = aktualni_datum
   
    def dodaj_datum(self, datum):
        self.datumi[datum] = Stanje(dnevnik="")

    def v_slovar(self):
        return {
            "datumi": {datum: stanje.v_slovar() for datum, stanje in self.datumi.items()},
            "aktualni_datum": self.aktualni_datum
        } 
    
    @staticmethod
    def iz_slovarja(slovar):
        koledar = Koledar()
        koledar.datumi = {
            datum: Stanje.iz_slovarja(stanje) for datum, stanje in slovar["datumi"].items()
        }
        if slovar["aktualni_datum"] == "None":
            koledar.aktualni_datum = None
        else:
            koledar.aktualni_datum = slovar["aktualni_datum"]
        return koledar
    
# ========================================================================================================================

class Stanje:
    def __init__(self, dnevnik):
        self.spiski = []
        self.aktualni_spisek = None
        self.dnevnik = dnevnik
    
    def dodaj_spisek(self, spisek):
        self.spiski.append(spisek)
        if not self.aktualni_spisek:
            self.aktualni_spisek = spisek
    
    def izbrisi_spisek(self, spisek):        # !!!!!!
        self.spiski.remove(spisek)
    
    def dodaj_opravilo(self, opravilo):
        self.aktualni_spisek.dodaj_opravilo(opravilo)
    
    def izbrisi_opravilo(self, opravilo):
        self.aktualni_spisek.izbrisi_opravilo(opravilo)

    def v_slovar(self):
        return {
            "spiski": [spisek.v_slovar() for spisek in self.spiski],
            "aktualni_spisek": self.spiski.index(self.aktualni_spisek)
            if self.aktualni_spisek
            else None,
            "dnevnik": self.dnevnik,
        }

    @staticmethod
    def iz_slovarja(slovar):
        stanje = Stanje(slovar["dnevnik"])
        stanje.spiski = [
            Spisek.iz_slovarja(sl_spiska) for sl_spiska in slovar["spiski"]
        ]
        if slovar["aktualni_spisek"] is not None:
            stanje.aktualni_spisek = stanje.spiski[slovar["aktualni_spisek"]]
        return stanje

# ========================================================================================================================

class Spisek:
    def __init__(self, ime):
        self.ime = ime
        self.opravila = []

    def dodaj_opravilo(self, opravilo):
        self.opravila.append(opravilo)
    
    def izbrisi_opravilo(self, opravilo):
        self.opravila.remove(opravilo)

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
import json

class Koledar:
    def __init__(self, datumi=None, aktualni_datum=None):
        self.datumi = datumi    # datumi je slovar stanj. Ključi so datumi, vrednosti so stanja
        self.aktualni_datum = aktualni_datum 
   
    def dodaj_datum(self, datum):
        self.datumi[datum] = Stanje()

    def v_slovar(self):
        datum_slovar = {}
        for datum, stanje in self.datumi.items():
            datum_slovar[datum] = {"obveznosti_dneva" : stanje.v_slovar()}
        return {
            "datumi": datum_slovar,
            "aktualni_datum": self.aktualni_datum,
        } 
    
    @staticmethod
    def iz_slovarja(slovar):
        koledar = Koledar()
        koledar.datumi = {
            datum: Stanje.iz_slovarja(stanje["obveznosti_dneva"]) for datum, stanje in slovar["datumi"].items()
        }
        if slovar["aktualni_datum"] == "None":
            koledar.aktualni_datum = None
        else:
            koledar.aktualni_datum = slovar["aktualni_datum"]
        return koledar

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return Koledar.iz_slovarja(slovar)

# ========================================================================================================================

class Dnevnik:
    def __init__(self, dnevniski_zapis):
        self.dnevniski_zapis = dnevniski_zapis  # niz, nič posebnega, samo besedilo

    def v_slovar(self):
        return {
            "dnevnik": self.dnevniski_zapis
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Dnevnik(
            slovar["dnevnik"],
        )
    
# ========================================================================================================================

# VSE OD TUKAJ DOL SPADA POD "obveznosti_dneva"

class Stanje:
    def __init__(self):
        self.spiski = []
        self.aktualni_spisek = None
    
    def dodaj_spisek(self, spisek):
        self.spiski.append(spisek)
        if not self.aktualni_spisek:
            self.aktualni_spisek = spisek
    
    def izbrisi_spisek(self, spisek):        # VKLJUČI!!!!!!
        self.spiski.remove(spisek)
    
    def zamenjaj_spisek(self, spisek):
        self.aktualni_spisek = spisek
    
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

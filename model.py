import json

class Koledar:
    pass


class Spisek:
    def __init__(self, ime):
        self.ime = ime
        self.opravila = []

    def dodaj_opravilo(self, opravilo):
        self.opravila.append(opravilo)

#############


class Opravilo:
    def __init__(self, ime, opis):
        self.ime = ime
        self.opis = opis 



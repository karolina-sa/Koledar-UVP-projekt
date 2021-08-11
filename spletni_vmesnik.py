import bottle
from model import Stanje, Spisek, Opravilo
import model
from datetime import datetime
import calendar
import json

IME_DATOTEKE = "stanje.json"
try:
    stanje = Stanje.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    stanje = Stanje()

#========================================================================================================================

@bottle.get('/')
def osnovna_stran():
    return bottle.template(
        "osnovna_stran.html",
        opravila=stanje.aktualni_spisek.opravila if stanje.aktualni_spisek else [],
        spiski=stanje.spiski,
        aktualni_spisek=stanje.aktualni_spisek
    )


@bottle.get('/izberi-datum/')
def izberi_datum():
    return bottle.redirect('/')


# OPRAVILA:

@bottle.post('/dodaj-opravilo/')
def dodaj_opravilo():
    ime = bottle.request.forms.getunicode("ime")
    opis = bottle.request.forms.getunicode("opis")
    opravilo = Opravilo(ime, opis)
    stanje.dodaj_opravilo(opravilo)
    stanje.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


# SPISKI:

@bottle.post('/dodaj-spisek/')
def dodaj_spisek():
    ime = bottle.request.forms.getunicode("ime")
    spisek = Spisek(ime)
    stanje.dodaj_spisek(spisek)
    stanje.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect('/')

@bottle.post("/dodaj-spisek/")
def dodaj_spisek_post():
    ime = bottle.request.forms.getunicode("ime")
    spisek = Spisek(ime)
    stanje.dodaj_spisek(spisek)
    stanje.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


@bottle.post('/zamenjaj-aktualni-spisek/')
def zamenjaj_aktualni_spisek():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    spisek = stanje.spiski[int(indeks)]
    stanje.aktualni_spisek = spisek
    stanje.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")




#========================================================================================================================

@bottle.error(404)
def error_404(error):
    return 'Ta stran ne obstaja.'

bottle.run(debug=True, reloader=True)
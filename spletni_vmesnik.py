import json
import bottle
from model import Koledar, Dnevnik, Opravilo, Spisek, Stanje

IME_DATOTEKE = "stanje.json"
try:
    koledar = Koledar.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    koledar = Koledar()

#========================================================================================================================

@bottle.get('/')
def osnovna_stran():
    return bottle.template(
        "osnovna_stran.html",
        datumi=koledar.datumi,
        aktualni_datum=koledar.aktualni_datum,
        opravila=koledar.datumi[koledar.aktualni_datum].aktualni_spisek.opravila if koledar.datumi[koledar.aktualni_datum].aktualni_spisek else [],
        spiski=koledar.datumi[koledar.aktualni_datum].spiski,  
        aktualni_spisek=koledar.datumi[koledar.aktualni_datum].aktualni_spisek
        # tukaj pride še za dnevnik
    )


# DATUM:

@bottle.post('/zamenjaj-datum/')
def zamenjaj_datum():
    print(dict(bottle.request.forms))
    datum = bottle.request.forms.getunicode("datum")
    if '-' in datum:
        if datum not in koledar.datumi.keys():
            koledar.dodaj_datum(datum)
        koledar.aktualni_datum = datum
        koledar.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect('/')

# OPRAVILA:

@bottle.post('/dodaj-opravilo/')
def dodaj_opravilo():
    ime = bottle.request.forms.getunicode("ime")
    opis = bottle.request.forms.getunicode("opis")
    opravilo = Opravilo(ime, opis)
    if ime not in 1000000 * ' ':
        koledar.datumi[koledar.aktualni_datum].dodaj_opravilo(opravilo)
        koledar.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect('/')

@bottle.post('/izbrisi-opravilo/')
def izbrisi_opravilo():
    indeks = bottle.request.forms.getunicode("indeks")
    opravilo = koledar.datumi[koledar.aktualni_datum].aktualni_spisek.opravila[int(indeks)]
    koledar.datumi[koledar.aktualni_datum].izbrisi_opravilo(opravilo)
    koledar.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect('/')


# SPISKI:

@bottle.post('/dodaj-spisek/')
def dodaj_spisek():
    ime = bottle.request.forms.getunicode("ime")
    spisek = Spisek(ime)
    if ime not in 1000000 * ' ':
        koledar.datumi[koledar.aktualni_datum].dodaj_spisek(spisek)
        koledar.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect('/')

#@bottle.post('/izbrisi-spisek/')        # NE DELA !!!!!!!!!!!!!!!!!!
#def izbrisi_spisek():
#    spisek = koledar.datumi[koledar.aktualni_datum].spiski[koledar.datumi[koledar.aktualni_datum].aktualni_spisek]
#    koledar.datumi[koledar.aktualni_datum].spiski.izbrisi_spisek(spisek)
#    koledar.shrani_v_datoteko(IME_DATOTEKE)
#    bottle.redirect('/')

@bottle.post('/zamenjaj-aktualni-spisek/')
def zamenjaj_aktualni_spisek():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    spisek = koledar.datumi[koledar.aktualni_datum].spiski[int(indeks)]
    koledar.datumi[koledar.aktualni_datum].aktualni_spisek = spisek
    koledar.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

#========================================================================================================================

@bottle.error(404)
def error_404(error):
    return 'Ta stran ne obstaja.'

bottle.run(debug=True, reloader=True)

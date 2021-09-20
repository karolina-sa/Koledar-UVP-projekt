import json
import bottle
from model import Koledar, Opravilo, Spisek, Stanje

IME_DATOTEKE = "stanje.json"
try:
    koledar = Koledar.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    koledar = Koledar()

@bottle.get('/opis-programa/')
def opis_programa_get():
    return bottle.template('opis_programa.html')

@bottle.get('/registracija/')
def registracija_get():
    return bottle.template('registracija.html')

@bottle.get('/img/<picture>')
def serve_pictures(picture):
    return bottle.static_file(picture, root='img')

#========================================================================================================================

@bottle.get('/')
def osnovna_stran():
    return bottle.template(
        "osnovna_stran.html",
        datumi=koledar.datumi,
        aktualni_datum=koledar.aktualni_datum,
        opravila=koledar.datumi[koledar.aktualni_datum].aktualni_spisek.opravila if koledar.datumi[koledar.aktualni_datum].aktualni_spisek else [],
        spiski=koledar.datumi[koledar.aktualni_datum].spiski,  
        aktualni_spisek=koledar.datumi[koledar.aktualni_datum].aktualni_spisek,
        dnevnik=koledar.datumi[koledar.aktualni_datum].dnevnik
    )


# DATUM:

@bottle.post('/zamenjaj-datum/')
def zamenjaj_datum():
    datum = bottle.request.forms.getunicode("datum")
    if '-' in datum:
        if datum not in koledar.datumi.keys():
            koledar.dodaj_datum(datum)
        koledar.aktualni_datum = datum
        koledar.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect('/')


# DNEVNIK:

@bottle.post('/dodaj-v-dnevnik/')
def dodaj_v_dnevnik():
    dnevnik = bottle.request.forms.getunicode("dnevnik")
    koledar.datumi[koledar.aktualni_datum].dnevnik = dnevnik
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
    imena_spiskov = []
    for s in koledar.datumi[koledar.aktualni_datum].spiski:
        imena_spiskov.append(s.ime)
    if ime not in 1000000 * ' ' and ime not in imena_spiskov:   # ne moreš dodat praznega spiska ali spiska, ki že obstaja
        koledar.datumi[koledar.aktualni_datum].dodaj_spisek(spisek)
        koledar.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect('/')

@bottle.post('/izbrisi-spisek/')        # NE DELA !!!!!!!!!
def izbrisi_spisek():
    spisek = koledar.datumi[koledar.aktualni_datum].aktualni_spisek
    koledar.datumi[koledar.aktualni_datum].izbrisi_spisek(spisek)
#    mesto = koledar.datumi[koledar.aktualni_datum].find(spisek)
#    if mesto == 0:
#        # mora bit aktualni spisek null
#    else:
#        # novo mesto bo mesto - 1
    if len(koledar.datumi[koledar.aktualni_datum].spiski) == 0:
        koledar.datumi[koledar.aktualni_datum].aktualni_spisek = None
    else:
        koledar.datumi[koledar.aktualni_datum].aktualni_spisek = koledar.datumi[koledar.aktualni_datum].spiski[0]
    koledar.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect('/')

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

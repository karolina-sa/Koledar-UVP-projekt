import bottle
from model import Uporabnik, Koledar, Stanje, Spisek, Opravilo

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "to je ena skrivnost"


def shrani_stanje(uporabnik):
    uporabnik.shrani_v_datoteko()

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")

def podatki_uporabnika(uporabnisko_ime):
    try:
        return Uporabnik.preberi_iz_datoteke(uporabnisko_ime)
    except FileNotFoundError:
        bottle.redirect("/prijava/")


@bottle.get('/registracija/')
def registracija_get():
    return bottle.template('registracija.html', napaka=None)

@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if geslo_v_cistopisu in 1000000 * ' ' or uporabnisko_ime in 1000000 * ' ':
        return bottle.template("registracija.html", napaka="Uporabniško ime in geslo ne smeta biti prazna niza.")
    else:
        if not uporabnisko_ime:
            return bottle.template("registracija.html", napaka="Vnesite uporabniško ime.")
        try:
            Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
            bottle.response.set_cookie(
                PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
            )
            bottle.redirect("/")
        except ValueError:
            return bottle.template("registracija.html", napaka="Uporabniško ime je že zasedeno.")


@bottle.get('/prijava/')
def prijava_get():
    return bottle.template("prijava.html", napaka=None)

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("prijava.html", napaka="Vnesi uporabniško ime.")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect("/")
    except ValueError:
        return bottle.template("prijava.html", napaka="Napačno uporabniško ime ali geslo. Za uporabo programa morate biti registrirani.")

@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")

#========================================================================================================================

@bottle.get('/')
def osnovna_stran():
    uporabnik = trenutni_uporabnik()
    return bottle.template(
        "osnovna_stran.html",
        koledar=uporabnik.koledar,
        datumi=uporabnik.koledar.datumi,
        aktualni_datum=uporabnik.koledar.aktualni_datum,
        opravila=uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].aktualni_spisek.opravila if uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].aktualni_spisek else [],
        spiski=uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].spiski,  
        aktualni_spisek=uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].aktualni_spisek,
        dnevnik=uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].dnevnik,
        uporabnik=uporabnik,
    )


# DATUM:

@bottle.post('/zamenjaj-datum/')
def zamenjaj_datum():
    uporabnik = trenutni_uporabnik()
    datum = bottle.request.forms.getunicode("datum")
    if '-' in datum:
        if datum not in uporabnik.koledar.datumi.keys():
            uporabnik.koledar.dodaj_datum(datum)
        uporabnik.koledar.aktualni_datum = datum
    shrani_stanje(uporabnik)
    bottle.redirect('/')


# DNEVNIK:

@bottle.post('/dodaj-v-dnevnik/')
def dodaj_v_dnevnik():
    uporabnik = trenutni_uporabnik()
    dnevnik = bottle.request.forms.getunicode("dnevnik")
    uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].dnevnik = dnevnik
    shrani_stanje(uporabnik)
    bottle.redirect('/')


# OPRAVILA:

@bottle.post('/dodaj-opravilo/')
def dodaj_opravilo():
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.forms.getunicode("ime")
    opis = bottle.request.forms.getunicode("opis")
    opravilo = Opravilo(ime, opis)
    if ime not in 1000000 * ' ':
        uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].dodaj_opravilo(opravilo)
    shrani_stanje(uporabnik)
    bottle.redirect('/')

@bottle.post('/izbrisi-opravilo/')
def izbrisi_opravilo():
    uporabnik = trenutni_uporabnik()
    indeks = bottle.request.forms.getunicode("indeks")
    opravilo = uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].aktualni_spisek.opravila[int(indeks)]
    uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].izbrisi_opravilo(opravilo)
    shrani_stanje(uporabnik)
    bottle.redirect('/')


# SPISKI:

@bottle.post('/dodaj-spisek/')
def dodaj_spisek():
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.forms.getunicode("ime")
    spisek = Spisek(ime)
    imena_spiskov = []
    for s in uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].spiski:
        imena_spiskov.append(s.ime)
    if ime not in 1000000 * ' ' and ime not in imena_spiskov:   # ne moreš dodat praznega spiska ali spiska, ki že obstaja
        uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].dodaj_spisek(spisek)
    shrani_stanje(uporabnik)
    bottle.redirect('/')

@bottle.post('/izbrisi-spisek/')       
def izbrisi_spisek():
    uporabnik = trenutni_uporabnik()
    spisek = uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].aktualni_spisek
    uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].izbrisi_spisek(spisek)
    if len(uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].spiski) == 0:
        uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].aktualni_spisek = None
    else:
        uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].aktualni_spisek = uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].spiski[0]
    shrani_stanje(uporabnik)
    bottle.redirect('/')

@bottle.post('/zamenjaj-aktualni-spisek/')
def zamenjaj_aktualni_spisek():
    uporabnik = trenutni_uporabnik()
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    spisek = uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].spiski[int(indeks)]
    uporabnik.koledar.datumi[uporabnik.koledar.aktualni_datum].aktualni_spisek = spisek
    shrani_stanje(uporabnik)
    bottle.redirect("/")

#========================================================================================================================

# DRUGO:

@bottle.get('/opis-programa-prijavljen/')
def opis_programa_get():
    uporabnik = trenutni_uporabnik()
    return bottle.template('opis_programa.html', uporabnik=uporabnik)

@bottle.get('/opis-programa/')
def opis_programa_get():
    return bottle.template('opis_programa.html')

@bottle.get('/img/<picture>')
def serve_pictures(picture):    # ker bottle nima za slike
    return bottle.static_file(picture, root='img')

#========================================================================================================================

@bottle.error(404)
def error_404(error):
    return 'Ta stran ne obstaja.'

bottle.run(debug=True, reloader=True)

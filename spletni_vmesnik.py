import bottle
from model import Koledar, Spisek, Opravilo

@bottle.get('/')
def osnovna_stran():
    return bottle.template('osnovna_stran.html')







@bottle.error(404)
def error_404(error):
    return 'Ta stran ne obstaja.'

bottle.run(debug=True, reloader=True)
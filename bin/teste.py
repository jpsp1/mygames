import web
import hashlib
import re
import sys

urls = (
   '/', 'Index',
   '/login', 'Login',
   '/logout', 'Logout',
   '/MGaddGame', 'MGaddGame',
   '/MPaddPlayer', 'MPaddPlayer',
)

passwdSalt='jpspPasswdSalt2693214585'

# "sessions doesn't work in debug mode because it interfere with reloading"
#web.config.debug = False
web.config.debug = True


app = web.application(urls, globals())

db = web.database(dbn='mysql', user='myTGames', pw='EXEK3jrmJjadHxvW', db='myTGames', host='localhost')

player_nameLC='joao'

listRes=db.select('player', where='nameLC=$player_nameLC',vars=locals())
print len(listRes)

sys.exit()


store = web.session.DBStore(db, 'sessions')

session = web.session.Session(app, store, initializer={'count': 0, 'login': 0,'privilege': 0,'user':'anonymous','loggedin':False})

web.config.session_parameters['cookie_name'] = 'webpy_session_id_jpsp_myTGames'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 3600
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'ndkj49hmawrh49hlhdb'
web.config.session_parameters['expired_message'] = 'Session expired'

render = web.template.render('templates/')


#---------------------------------- database
# uses web-sessions DB
# docs:
# http://webpy.org/cookbook/select
class DB:
    def playerAdd(self,player_name,player_age,player_lic):
        player_nameLC=player_name.lower()
        r=db.select('player', where='nameLC=$player_nameLC',vars=locals())[0]

#        ident['pass']:

        #        entries = db.select('mytable')
        #       results = db.select('players', myvar, where="name = $name")
        return 

# creates object
appDB=DB()



#--------------------------------------------
def logged():
    if session.login==1:
        return True
    else:
        return False

def okInputStr(str):
    p=re.compile('^[a-zA-Z0-9]*$')
    if len(str) > 1000:
        return False
    return p.match(str)

def okInputNumber(str):
    p=re.compile('^[0-9]*$')
    if len(str) > 1000:
        return False
    return p.match(str)

class Login(object):
    def GET(self):
        h = render.header() 
        f = render.footer(session) 
        return render.login2(unicode(h), unicode(f))
    def POST(self):
        name, passwd = web.input().user, web.input().passwd
        ident = db.select('users', where='user=$name', \
                          vars=locals())[0]
        passwd_enc=hashlib.sha1(passwdSalt+passwd).hexdigest()
        print name,passwd,passwd_enc
        if  passwd_enc == ident['pass']:
            session.login = 1
            session.user=web.input().user
            h = render.header() 
            f = render.footer(session) 
            return render.index(unicode(h), unicode(f))
        else:
            h = render.header() 
            f = render.footer(session) 
            return render.login_failed(unicode(h), unicode(f), web.input().user)

class Logout(object):
    def POST(self):
        session.login = 0
        session.user='anonymous'
        h = render.header() 
        f = render.footer(session) 
        return render.index(unicode(h), unicode(f))

class MGaddGame(object):
    def GET(self):
        if logged():
            h = render.header() 
            h2= render.MGmenu()
            f = render.footer(session) 
            return render.MGaddGame(unicode(h), unicode(h2), unicode(f))
        else:
            h = render.header() 
            f = render.footer(session) 
            return render.noLogin(unicode(h), unicode(f))

class MPaddPlayer(object):
    def GET(self):
        if logged():
            h = render.header() 
            h2= render.MPmenu()
            f = render.footer(session) 
            return render.MPaddPlayer(unicode(h), unicode(h2), unicode(f))
        else:
            h = render.header() 
            f = render.footer(session) 
            return render.noLogin(unicode(h), unicode(f))
    def POST(self):
        if logged():
            h = render.header() 
            h2= render.MPmenu()
            f = render.footer(session) 
            player_name,player_age,player_lic=\
                web.input().player_name, \
                web.input().player_age,\
                web.input().player_lic
            if not okInputStr(player_name):
                return render.syntaxErrorInput(unicode(h), unicode(f),player_name)
            if not okInputNumber(player_age):
                return render.syntaxErrorInput(unicode(h), unicode(f),player_age)
            if not okInputStr(player_lic):
                return render.syntaxErrorInput(unicode(h), unicode(f),player_lic)
            appDB.playerAdd(player_name,player_age,player_lic)
        else:
            h = render.header() 
            f = render.footer(session) 
            return render.noLogin(unicode(h), unicode(f))

class Index(object):
    def GET(self):
        h = render.header() 
        f = render.footer(session) 
        return render.index(unicode(h), unicode(f))

if __name__ == "__main__":
    app.run()


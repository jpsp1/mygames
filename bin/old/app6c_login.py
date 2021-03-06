import web
import hashlib

urls = (
   '/login', 'Login',
   '/logout', 'Logout',
   '/', 'Index',
)

passwdSalt='jpspPasswdSalt2693214585'

# "sessions doesn't work in debug mode because it interfere with reloading"
web.config.debug = False
#web.config.debug = True


app = web.application(urls, globals())

db = web.database(dbn='mysql', user='myTGames', pw='EXEK3jrmJjadHxvW', db='myTGames', host='localhost')

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





#--------------------------------------------
def logged():
    if session.login==1:
        return True
    else:
        return False

class Login(object):
    def GET(self):
        if logged():
            print "<html><head><title>already logged in. logout</title>" + \
          "</head><body><h1>lready logged in. logout</h1>" + \
         "</body></html>"
        else:
            render.login()
    def POST(self):
        name, passwd = web.input().user, web.input().passwd
        ident = db.select('users', where='user=$name', \
                          vars=locals())[0]
        passwd_enc=hashlib.sha1(passwdSalt+passwd).hexdigest()
        print name,passwd,passwd_enc
        if  passwd_enc == ident['pass']:
            session.login = 1
            print "<html><head><title>t</title>\
               </head><body><h1>user $name authenticated</h1>\
               </body></html>"
        else:
            session.login = 0
            print "<html><head><title>t</title>\
               </head><body><h1>user $name failed to auth</h1>\
               </body></html>"

class Logout(object):
    def GET(self):
        if logged():
            session.login = 0
            print "foi deslogado"
        else:
            print "nao esta logado"



class BD(object):
    def GET(self):
        db = web.database(dbn='mysql', user='myTGames', pw='EXEK3jrmJjadHxvW', db='myTGames', host='localhost')
        try:
           db.query("show tables")
        except:
           print "DB ERRO"
        else:
           print "DB OK"
        return render.hello_form()

    def POST(self):
        form = web.input(name="Nobody", greet="Hello")
        greeting = "%s, %s" % (form.greet, form.name)
        return render.index(greeting = greeting)


class Index(object):
    def GET(self):
        h = render.header() 
        f = render.footer(session) 
        return render.index(unicode(h), unicode(f))
#       session.count+=1
#       return render.index2(session=session)

if __name__ == "__main__":
    app.run()


import web

web.config.db_parameters = {
                            'dbn' : 'mysql',
                            'host' : 'localhost',
                            'user' : 'myTGames',
                            'pw' : 'EXEK3jrmJjadHxvW',
                            'db' : 'myTGames'
                    }

urls = (
   '/login', 'Login',
   '/', 'Index',
)

web.config.debug = False


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

class Login(object):
    def GET(self):
        return render.login()

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
       session.count+=1
       session.loggedin=True
       if session.get('loggedin', False):
            print "loggedin==TRUE"
       else:
            print "loggedin==FALSE"
       print "OOOOOOOOOOOOOOOOLA =", session, session.count

    def POST(self):
        form = web.input(name="Nobody", greet="Hello")
        greeting = "%s, %s" % (form.greet, form.name)
        return render.index(greeting = greeting)

if __name__ == "__main__":
    app.run()


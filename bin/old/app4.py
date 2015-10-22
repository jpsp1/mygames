import web

urls = (
  '/hello', 'Index',
  '/bd', 'BD',
)

app = web.application(urls, globals())

render = web.template.render('templates/')


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
        return render.hello_form()

    def POST(self):
        form = web.input(name="Nobody", greet="Hello")
        greeting = "%s, %s" % (form.greet, form.name)
        return render.index(greeting = greeting)

if __name__ == "__main__":
    app.run()


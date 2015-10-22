#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import web
import hashlib
import re
import datetime

config='/home/ec2-user/mygames/local/config.py'

execfile(config)

urls = (
   '/', 'Index',   
   '/l', 'Listagem01',  
   '/l1b', 'Listagem01b',
   '/l2', 'Listagem02',
   '/login', 'Login',
   '/logout', 'Logout',
)

# "sessions doesn't work in debug mode because it interfere with reloading"
web.config.debug = False
#web.config.debug = True

app = web.application(urls, globals())

db = web.database(dbn=config_dbn,
                  user=config_user,
                  pw=config_pw,
                  db=config_db,
                  host=config_host)

#----------
# inicializacao sessoes
passwdSalt='jpspPasswdSalt2693214585'
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'count': 0, 'login': 0,'privilege': 0,'user':'anonymous','loggedin':False})
# http://webpy.org/sessions/
web.config.session_parameters['cookie_name'] = 'webpy_session_id_jpsp_resul'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 3600
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'ndkj49hmawrh49hlhdb'
web.config.session_parameters['expired_message'] = 'Session expired'

render = web.template.render('templates/')

def okInputStr(str):
    # NOTA:\w com UNICODE inclui çáéíóúàèìòùãẽĩõũâêîôû e ÇÁÉÍÓÚÀÈÌÒÙÃẼĨÕŨÂÊÎÔÛ
    p=re.compile('^[a-zA-Z0-9\s\,\.\;\%\!\n\:\-\_\w]*$',flags=re.UNICODE)
    if len(str) > 4001:
        return False
    return p.match(str)

def okInputStrList(lista):
    for l in lista:
        if len(l)>0:
            if not okInputStr(l):
                return False
    return True

def okInputNumber(str):
    p=re.compile('^[0-9]*$')
    if len(str) > 1000:
        return False
    return p.match(str)

def corrige_int(str_n):
    if not okInputNumber(str_n):
        return 0;
    if len(str_n)<=0:
        return -1
    nr=int(str_n)
    if nr < 0:
        return 0;
    if nr > 2050:
        return 0;
    return nr

def faz_array(num,num_i,num_f):
    array=[]
    for i in range(num_i,num_f):
        if i==num:
            array.append('selected')
        else:
            array.append('        ')
    return array

def horario():
    now = datetime.datetime.now()
    if now.hour < 8 or  now.hour > 21:
        return False
    return True

def logged():
    if session.login==1:
        return True
    else:
        return False

#----------------------------- paginas

#-- login e logout
class Login(object):
    def GET(self):
        h = render.header(session)
        f = render.footer()
        return render.login(unicode(h), unicode(f))
    def POST(self):
        h = render.header(session)
        f = render.footer()
        name, passwd = web.input().user, web.input().passwd
        ident2 = db.select('users', where='user=$name', vars=locals())
        if len(ident2)==0:
            return render.login_failed(unicode(h), unicode(f), web.input().user)
        else:
            ident=ident2[0]
            passwd_enc=hashlib.sha1(passwdSalt+passwd).hexdigest()
            print name,passwd,passwd_enc
            if  passwd_enc == ident['pass']:
                session.login = 1
                session.user=web.input().user
                h = render.header(session) 
                f = render.footer() 
                return render.login_ok(unicode(h), unicode(f), web.input().user)
            else:
                h = render.header(session) 
                f = render.footer() 
                return render.login_failed(unicode(h), unicode(f), web.input().user)

class Logout(object):
    def GET(self):
        session.login = 0
        session.user='anonymous'
        h = render.header(session) 
        f = render.footer()
        return render.logout(unicode(h), unicode(f))


class Index(object):
    def GET(self):
        if not horario():
            return -3
        header = render.header(session)
        footer = render.footer()
        if not logged():
            return render.noLogin(unicode(header), unicode(footer))

        now = datetime.datetime.now()
        str_now=now.strftime("%d-%b-%Y %Hh%M")
        data_dia_selected=faz_array(now.day,1,32)
        data_mes_selected=faz_array(now.month,1,13)
        data_ano_selected=faz_array(now.year,2005,2023)
        data_hora_selected=faz_array(now.hour,0,24)
        return render.index(unicode(header),unicode(footer),
                            str_now,
                            data_dia_selected,
                            data_mes_selected,
                            data_ano_selected,
                            data_hora_selected,
                            )

    def POST(self):
        if not horario():
            return -3
        header = render.header(session)
        footer = render.footer()
        if not logged:
            return render.noLogin(unicode(header), unicode(footer))
        auth=web.input().auth
        u_reg=web.input().u_reg
        u_nreg=web.input().u_nreg
        l_reg=web.input().l_reg
        l_nreg=web.input().l_nreg
        data_dia=web.input().data_dia
        data_mes=web.input().data_mes
        data_ano=web.input().data_ano
        hora_hora=web.input().hora_hora
        hora_minuto=web.input().hora_minuto
        resultado=web.input().resultado
        Set01_eu=web.input().Set01_eu
        Set01_adv=web.input().Set01_adv
        Set02_eu=web.input().Set02_eu
        Set02_adv=web.input().Set02_adv
        Set03_eu=web.input().Set03_eu
        Set03_adv=web.input().Set03_adv
        res_desc=web.input().res_desc
        vars=[
            auth,
            u_reg,
            u_nreg,
            l_reg,
            l_nreg,
            data_dia,
            data_mes,
            data_ano,
            hora_hora,
            hora_minuto,
            resultado,
            Set01_eu,
            Set01_adv,
            Set02_eu,
            Set02_adv,
            Set03_eu,
            Set03_adv,
            res_desc,
            ]
        if not okInputStrList(vars):
            return -1
        u_reg=corrige_int(u_reg)
        l_reg=corrige_int(l_reg)
        data_dia=corrige_int(data_dia)
        data_mes=corrige_int(data_mes)
        data_ano=corrige_int(data_ano)
        hora_hora=corrige_int(hora_hora)
        hora_minuto=corrige_int(hora_minuto)
        resultado=corrige_int(resultado)
        Set01_eu=corrige_int(Set01_eu)
        Set01_adv=corrige_int(Set01_adv)
        Set02_eu=corrige_int(Set02_eu)
        Set02_adv=corrige_int(Set02_adv)
        Set03_eu=corrige_int(Set03_eu)
        Set03_adv=corrige_int(Set03_adv)

        sequence_id = db.insert('game', 
                                auth=auth,
                                u_reg=u_reg,
                                u_nreg=u_nreg,
                                l_reg=l_reg,
                                l_nreg=l_nreg,
                                data_dia=data_dia,
                                data_mes=data_mes,
                                data_ano=data_ano,
                                hora_hora=hora_hora,
                                hora_minuto=hora_minuto,
                                resultado=resultado,
                                Set01_eu=Set01_eu,
                                Set01_adv=Set01_adv,
                                Set02_eu=Set02_eu,
                                Set02_adv=Set02_adv,
                                Set03_eu=Set03_eu,
                                Set03_adv=Set03_adv,
                                res_desc=res_desc,
                                )
        return render.index_res(            
            unicode(header),unicode(footer),
            u_reg,
            u_nreg,
            l_reg,
            l_nreg,
            data_dia,
            data_mes,
            data_ano,
            hora_hora,
            hora_minuto,
            resultado,
            Set01_eu,
            Set01_adv,
            Set02_eu,
            Set02_adv,
            Set03_eu,
            Set03_adv,
            res_desc,
            )

class Listagem01(object):
    def GET(self):
        if not horario():
            return -3
        header = render.header(session)
        footer = render.footer()
        if not logged():
            return render.noLogin(unicode(header), unicode(footer))
        return render.l(unicode(header),unicode(footer))

class Listagem02(object):
    def GET(self):
        if not horario():
            return -3
        header = render.header(session)
        footer = render.footer()
        if not logged():
            return render.noLogin(unicode(header), unicode(footer))
        return render.l2(unicode(header),unicode(footer))
    def POST(self):
        if not horario():
            return -3
        header = render.header(session)
        footer = render.footer()
        if not logged():
            return render.noLogin(unicode(header), unicode(footer))
        auth=web.input().auth
        u_reg=web.input().u_reg
        vars=[
            auth,
            u_reg,
            ]
        if not okInputStrList(vars):
            return -1
        #http://stackoverflow.com/questions/6053219/simple-way-to-display-results-of-a-sql-query-using-web-py
        #http://webpy.org/cookbook/select
        results =  db.select('game', 
                             where='u_reg=$u_reg',
                             order='id',
                             vars=locals(),
                             )
        return render.l2_res(unicode(header),unicode(footer),u_reg,results)

class Listagem01b(object):
    def GET(self):
        if not horario():
            return -3
        header = render.header(session)
        footer = render.footer()
        if not logged():
            return render.noLogin(unicode(header), unicode(footer))
        results =  db.select('player', 
                             order='nome',
                             vars=locals(),
                             )
        return render.l1b(unicode(header),unicode(footer),results)

if __name__ == "__main__":
    app.run()

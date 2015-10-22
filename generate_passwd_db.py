import hashlib

passwdSalt='jpspPasswdSalt2693214585'
passwd="app.python"
passwd_enc=hashlib.sha1(passwdSalt+passwd).hexdigest()
print passwd,passwd_enc




import htmlPy, json
import os, sys, time, datetime
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib
from securityApp import app as passwordManagerApp

KEY_LENGTH = 32

class RegisterData(htmlPy.Object):

    def __init__(self):
        super(RegisterData.self).__init__()
        return

    @htmlPy.Slot(str, result=str)
    def regNewInfo(self, data):
        if checkAuth('password', data.password, data.username):
            # Get decrypted intermediary key
            key = self.decryptKey('password', data.password, data.username)
            # Open iv to encrypt data info
            iv = open('../data/security/iv_data_' + str(KEY_LENGTH/2) + '_' + data.username + '.txt').read()
            # Open data info file
            df = open('../data/info/' + data.infoName + '_enc_' + user + '_' + self.genTimestamp() + '.txt', 'w')
            # Pad data info
            dfPad = self.pad(df, len(key))

            # Create the cipher object and process the input stream
            cipher = AES.AESCipher(key, AES.MODE_CBC, iv)

            encData = iv + cipher.encrypt(dfPad))

            df.write(encData)
            df.close()
            key = None
            return true
        else return 'Senha incorreta!'

    def checkAuth(self, fileType, pw, user):
        hf = open('../data/security/hash_' + fileType + '_' + user + '.txt', 'rb').read()
        hash = hashlib.sha256(pw).hexdigest()
        if(hash == hf) return true
        else return false

    def decryptKey(self, fileType, pw, user):
        # Read password salt and iv
        iv = open('../data/security/iv_'  + fileType + '_' + str(KEY_LENGTH/2) + '_' + user + '.txt', 'rb').read()
        salt = open('../data/security/salt_'  + fileType + '_' + str(KEY_LENGTH) + '_' + user + '.txt', 'rb').read()

        # Read encrypted intermediary key
        enc = open('../data/security/aes_' + fileType + '_enc_' + str(KEY_LENGTH) + '_' + user + '.key' , 'rb').read()

        # Generate KDF secret key
        pk = KDF.PBKDF2(pw, salt, KEY_LENGTH, 1000, None)

        # Create the cipher object and decrypt intermediary key with KDF secret key
        cipher = AES.AESCipher(pk, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[len(pk)/2:]))

    def genTimestamp(self):
        return time.mktime(datetime.datetime.now().timetuple())

    def pad(self, s, bs):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    def unpad (self, s):
        return s[0:-ord(s[-1])]

passwordManagerApp.bind(RegisterData())
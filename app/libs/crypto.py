import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

class Crypto(object):

    def __init__(self, code):
        self.block_size = 16
        self.code = code

    def pad(self, s):
        return s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def get_private_key(self):
        salt = b"this is a salt"
        kdf = PBKDF2(self.code, salt, 64, 1000)
        key = kdf[:32]
        return key


    def encrypt(self, raw):
        private_key = self.get_private_key()
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        r = base64.b64encode(iv + cipher.encrypt(raw.encode("UTF-8"))).decode('utf-8')
        print(r)
        return r


    def decrypt(self, enc):
        # enc = self.pad(enc)
        print(enc)
        private_key = self.get_private_key()
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return bytes.decode(self.unpad(cipher.decrypt(enc[16:])))


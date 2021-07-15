from elgamal.elgamal import Elgamal

class ElgamalCrypto:
    def __init__(self,n_bits=128):
        self.n_bits=n_bits

    def gen_key(self):
        pb,pv=Elgamal.newkeys(self.n_bits)
        return pb,pv

    def encode(self,message,public_key):
        return Elgamal.encrypt(message,public_key)

    def decode(self,message,private_key):
        return Elgamal.decrypt(message,private_key)
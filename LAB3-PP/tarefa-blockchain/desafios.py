import hashlib

from attr import has
class Challenge:
    def __init__(self, transactionID, challenge):
        self.transactionID = transactionID
        self.challenge = challenge
        self.clientID = -1
    
    def hash_seed(seed):
        a = hashlib.sha1(seed.encode())
        b = a.hexdigest()
        return str(bin(int(b, 16)))[2:]

    def check_seed(self, seed):
        if self.clientID != -1:
            return False
        x = self.hash_seed(seed)
        return x.startsWith("0"*self.challenge)
    
    def get_winner(self):
        return self.clientID

    def encode_challenge(self):
        return str(self.transactionID)+ "/" + str(self.challenge)
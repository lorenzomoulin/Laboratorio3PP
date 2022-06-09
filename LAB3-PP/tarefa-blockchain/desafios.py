class Challenge:
    def __init__(self, transactionID, challenge):
        self.transactionID = transactionID
        self.challenge = challenge
        self.clientID = -1
    
    def check_seed(self, seed):
        pass
    
    def get_winner(self):
        return self.clientID

    def encode_challenge(self):
        return str(self.transactionID)+ "/" + str(self.challenge)
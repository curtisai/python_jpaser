from token_type import TokenType

class Token:

    def __init__(self, the_type = TokenType.NULL):
        self.type = the_type

    def getType(self):
        return self.type

    def setType(self, new_type ):
        self.type = new_type

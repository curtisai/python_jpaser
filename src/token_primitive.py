from token import Token
from token_type import TokenType

class TokenPrimitive( Token ) :
    def __init__(self, type = TokenType.NULL, value = None):
        Token.__init__(self, type)
        self.value = value

    def getValue(self):
        return self.value


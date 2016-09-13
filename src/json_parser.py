from token_primitive import TokenPrimitive
from json_entity import JsonEntity
from jentity_type import JEntityType
from token import Token
from token_type import TokenType
import re

from jparser_exception import JsonException

class JsonParser:

    def __init__( self, new_json = None ):
        self.json = new_json
        self.index = -1

    # Get the next token from json string
    def getToken( self ):
        self.index += 1

        if  self.index >= len( self.json ):
            return TokenType.NULL

        current_char = self.json[self.index]

        # Skip all spaces and returns
        while current_char == ' ' or current_char == '\r' or current_char == '\n':
            self.index += 1
            current_char = self.json[self.index]


        if   current_char == '{':
            return Token( TokenType.OPEN_BRACE )
        elif current_char == '}':
            return Token( TokenType.CLOSE_BRACE )
        elif current_char == '[':
            return Token( TokenType.OPEN_BRACKET )
        elif current_char == ']':
            return Token( TokenType.CLOSE_BRACKET )
        elif current_char == '\"' or current_char == '\'':
            return self.parseString()
        elif current_char == 't' or current_char == 'f':
            return self.parseBoolean()
        elif current_char == 'n':
            return self.parseNull()
        elif current_char == ',':
            return Token( TokenType.COMMA )
        elif current_char == ':':
            return Token( TokenType.COLON )
        elif   current_char == '0' \
            or current_char == '1' \
            or current_char == '2' \
            or current_char == '3' \
            or current_char == '4' \
            or current_char == '5' \
            or current_char == '6' \
            or current_char == '7' \
            or current_char == '8' \
            or current_char == '9' \
            or current_char == '-' :
            return self.parseNumber()
        else:
            raise JsonException( "unknown token found at position " + str( self.index ) )



    def parseString( self ):
        self.index += 1
        start = self.index

        # Find the end of the string
        while       self.index < len( self.json ) \
                and self.json[self.index] != '\"' \
                and self.json[self.index] != '\'' :
            self.index += 1

        return TokenPrimitive( TokenType.STRING, str( self.json[ start : self.index ] ) )



    def parseBoolean( self ):
        if self.json[ self.index : self.index + 4 ] == "false":
            self.index += 5
            return TokenPrimitive( TokenType.BOOLEAN, False )
        elif self.json[ self.index, self.index + 3 ] == "true":
            self.index += 4
            return TokenPrimitive( TokenType.BOOLEAN, True )
        else:
            raise JsonException( "Parsing Boolean Error at position " + str( self.index ) )

    def parseNull( self ):
        if self.json[self.index:self.index + 3] == "null":
            self.index += 4
            return TokenPrimitive( TokenType.NULL, None )
        else:
            raise JsonException( "Parsing Null Error at position " + str( self.index ) )

    def parseNumber( self ):
        # Mark the start position of number
        start = self.index
        # Find the first character that isn't a number
        int_end = re.search( "[0-9]", self.json[self.index + 1:] )

        if int_end:
            self.index += int_end.end() + 1
        # Check if it's float
        if self.json[self.index + 1] == '.':
            decimal_end = re.search( "[0-9]", self.json[self.index + 2:] )
            if decimal_end:
                self.index += decimal_end.end() + 1

        try:
            return TokenPrimitive( TokenType.INTEGER, int(self.json[start:self.index + 1]))
        except ValueError:
            return TokenPrimitive( TokenType.DOUBLE, float(self.json[start:self.index + 1]))


    def createArray( self ):
        the_array = []
        expected_token = Token()

        while True:
            current_token = self.getToken()
            if current_token.getType() == TokenType.NULL:
                raise JsonException( "Parsing Array Error at Position " + str( self.index ) + ": end of json" )

            if     (    expected_token.getType() != TokenType.NULL \
                    and current_token.getType() != expected_token.getType() \
                    and current_token.getType() != TokenType.CLOSE_BRACKET ) \
                or (    expected_token.getType() != TokenType.COMMA \
                    and current_token.getType() == TokenType.CLOSE_BRACKET \
                   ):
                raise JsonException( "Parsing Array Error at Position " + str( self.index ) + ": invalid argument" )

            if   current_token.getType() == TokenType.COMMA:
                expected_token.setType( TokenType.NULL )
            elif current_token.getType() == TokenType.STRING:
                the_array.append( self.createString( current_token ) )
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.INTEGER:
                the_array.append( self.createInt( current_token ) )
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.DOUBLE:
                the_array.append( self.createDouble( current_token ) )
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.BOOLEAN:
                the_array.append( self.createBoolean( current_token ) )
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.OPEN_BRACKET:
                the_array.append( self.createArray() )
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.OPEN_BRACE:
                the_array.append( self.createObject() )
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.CLOSE_BRACKET:
                return JsonEntity( the_array, JEntityType.ARRAY )
            else:
                raise JsonException( "createArray: invalid token at position " + str( self.index) )

    def createString( self, input_token ):
        return JsonEntity( input_token.getValue(), JEntityType.STRING )

    def createInt( self, input_token ):
        return JsonEntity( input_token.getValue(), JEntityType.INTEGER )

    def createDouble( self, input_token ):
        return JsonEntity( input_token.getValue(), JEntityType.DOUBLE )

    def createBoolean( self, input_token ):
        return JsonEntity( input_token.getValue(), JEntityType.BOOLEAN )

    def createObject( self ):
        json_entity_map = dict()
        expected_token = Token( TokenType.STRING )
        json_value = JsonEntity()
        json_key = None

        while True:
            current_token = self.getToken()

            if ( (     expected_token.getType() != TokenType.NULL \
                   and current_token.getType() != expected_token.getType() \
                   and current_token.getType() != TokenType.CLOSE_BRACE ) ) \
                or (   expected_token.getType() != TokenType.COMMA \
                   and current_token.getType() == TokenType.CLOSE_BRACE ):

                raise JsonException( "createObject: Invalid token at position " + str( self.index ) )

            if current_token.getType() == TokenType.COLON:
                expected_token.setType( TokenType.NULL )
            elif current_token.getType() == TokenType.COMMA:
                json_entity_map[json_key] = json_value
                expected_token.setType( TokenType.STRING )
            elif current_token.getType() == TokenType.STRING:
                if expected_token.getType() == TokenType.STRING:
                    json_key = str( current_token.getValue() )
                    expected_token.setType( TokenType.COLON )
                else:
                    json_value = self.createString( current_token )
                    expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.INTEGER:
                json_value = self.createInt( current_token )
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.DOUBLE:
                json_value = self.createDouble( current_token )
                expected_token.setType(( TokenType.COMMA ) )
            elif current_token.getType() == TokenType.OPEN_BRACE:
                json_value = self.createObject()
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.OPEN_BRACKET:
                json_value = self.createArray()
                expected_token.setType( TokenType.COMMA )
            elif current_token.getType() == TokenType.CLOSE_BRACE:
                json_entity_map[json_key] = json_value
                return JsonEntity( json_entity_map, JEntityType.OBJECT )
            else:
                raise JsonException( "createObject: Invalid token at position " + str( self.index ) )

    def fromString(self, input_json):
        self.json = input_json
        self.index = -1
        current_token = self.getToken()
        if current_token.getType() == TokenType.OPEN_BRACE:
            return self.createObject()
        elif current_token.getType() == TokenType.OPEN_BRACKET:
            return self.createArray()
        else:
            raise JsonException( "Invalid input" )
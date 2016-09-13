from jentity_type import JEntityType

class JsonEntity:
    def __init__( self, content = None, type = JEntityType.UNKNOWN ):
        self.entity_type = type
        self.content = content

    def getType( self ):
        return self.entity_type

    def getContent( self ):
        return self.content

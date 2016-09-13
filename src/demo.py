from json_parser import JsonParser
from jparser_exception import JsonException

my_parser = JsonParser()


json = '''{"glossary":{"title": "example glossary","GlossDiv":{"title":"S","GlossList":{"GlossEntry": {"ID": "SGML","SortAs": "SGML","GlossTerm": "Standard Generalized Markup Language","Acronym":"SGML","Abbrev": "ISO 8879:1986","GlossDef": {"para": "A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso": ["GML", "XML"]},"GlossSee": "markup"}}}}}'''

json2 = '''{"glossary": -12.1 , "yes" : "how" }'''

invalid_json = '''{"glossary": -12.1s, "yes" : "how" }'''

result = my_parser.fromString( json )

result2 = my_parser.fromString( json2 )

print result.getContent()["glossary"].getContent()["title"].getContent()
# Should print example glossary

print result.getContent()["glossary"].getContent()["GlossDiv"].getContent()["GlossList"].getContent()["GlossEntry"].getContent()["ID"].getContent()
# Should print SGML

print result2.getContent()["glossary"].getContent()
# Should print -12.1

try:
    result3 = my_parser.fromString( invalid_json )
except JsonException as exp:
    print exp.message
# Should raise an exception indicates syntax error at position 18



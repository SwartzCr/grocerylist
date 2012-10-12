import sys
import email as e
from email.parser import Parser 

def parse(email):
    pip = Parser()
    message = Parser.parsestring(pip , email)
    return(message)

def strip_body()
    y = message.keys()
    # x = message.getitem('body')
    x = ""
    for key in y:
        x +=str(key)+"\n"
    with open("/home/swartzcr/scripts/test.txt", 'w') as f:
        f.write(x)
    

import sys
import email as e
from email.parser import Parser 
import unittest


def parse(email):
    pip = Parser()
    message = Parser.parsestring(pip , email)
    return(message)

def strip_body(message):
    body = message.do_some_magic()
    return body

def body2grocery_items(body):
    return ['celery', 'guanine']

def items_to_file(items, fileobj):
    for item in items:
        fileobj.writeline(item)

class AutomtedTest(unittest.TestCase):
    def test_body_extraction(self):
        result = body2grocery_items('''celery
cytosine''')
        self.assertEqual(['celery', 'cytosine'],
                        result)

    def test_complete_thing(self):
        sample_file = open('my-sample-message').read()
        parsed = parse(sample_file)
        body = strip_body(parsed)
        items = body2grocery_items(body)
        self.assertEqual(['celery', 'cytosine'], items)
    

#    y = message.keys()
#    # x = message.getitem('body')
#    x = ""
#    for key in y:
#        x +=str(key)+"\n"
#    with open("/home/swartzcr/scripts/test.txt", 'w') as f:
#        f.write(x)


def main():
    email = sys.stdin.read()
    message = parse(email) 
    

if __name__ == "__main__":
    unittest.main()
            

import sys
import email  
from email.parser import Parser 
import unittest


def parse(email_text):
    message = email.message_from_string(email_text)
    return(message)

def strip_body(message):
    body = message.get_payload()
    for load in body:
        if load.get_content_type() == 'text/plain':
            return load.get_payload()

def body2grocery_items(body):
    print body
    print type(body)
    body = body.splitlines()
    return body

def items_to_file(items, fileobj):
    for item in items:
        fileobj.writeline(item)

def add_items2list(items, old_list):
    with open(old_list) as f:
        cur_list = f.read()
    for item in items:
        cur_list = cur_list + item + "\n"
    return cur_list

def write_list(new_list, list_filename):
    with open(list_filename, 'w') as f:
        f.write(new_list)

class AutomtedTest(unittest.TestCase):
    def test_body_extraction(self):
        result = body2grocery_items('''celery
guanine''')
        self.assertEqual(['celery', 'guanine'],
                        result)

    def test_complete_thing(self):
        old_list = "test-grocery.txt"
        final_list = "test-final-list.txt"
        sample_file = open('test.txt').read()
        parsed = parse(sample_file)
        body = strip_body(parsed)
        items = body2grocery_items(body)
        new_list = add_items2list(items, old_list)
        write_list(new_list, old_list)
        self.assertEqual(old_list, final_list)
    

def main():
    old_list = "grocery.txt"
    email_text = sys.stdin.read()
    message = parse(email_text)
    body = strip_body(message)
    items = body2grocery_items(body)
    new_list = add_items2list(items, old_list)
    write_list(new_list, old_list) 
    

if __name__ == "__main__":
    #unittest.main()
    main()        

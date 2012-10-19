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

def parse_pagefile(path):
    with open(path) as f:
        page = f.read()
    page = page.split("<body>")
    new_page = []
    new_page.append(page[0])
    new_page.append("<body>")
    body_trail = page[1].split("</body>")
    new_page.append(body_trail[0])
    new_page.append("</body>")
    new_page.append(body_trail[1])
    return(new_page)

def add_items2list(items, body):
    num = len(x)
    for item in items:
        body.append(num+" "+item)
        num += 1
    return body

def list2string(sep_list):
    final_list = ""
    for item in sep_list:
        line = ""
        for part in item:
            line += part
        final_list += line+"\n"
    return final_list

def stitch(pagelist):
    page = ""
    for item in pagelist:
        page += item
    return page

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
    this_path = os.path.abspath("__this__")
    this_dir = os.path.dirname(this_path)
    pagefile_path = this_dir + "/index.html"
    pagefile = parse_pagefile(pagefile_path)
    pagefile_body = pagefile[2]
    email_text = sys.stdin.read()
    message = parse(email_text)
    body = strip_body(message)
    items = body2grocery_items(body)
    new_body = add_items2list(items, pagefile_body)
    pagefile[2] = new_body
    new_list = stitch(pagefile)
    write_list(new_list, pagefile_path) 
    

if __name__ == "__main__":
    #unittest.main()
    main()        

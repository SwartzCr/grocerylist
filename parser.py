import sys
import os.path
import email  
from email.parser import Parser 
import unittest
import json
import smtplib
from email.mime.text import MIMEText

def parse_email(email_data):
    parsed_email = email.message_from_string(email_data)
    return parsed_email

def parsed_email2split_lines(parsed_email):
    payloads = parsed_email.get_payload()
    for payload in payloads:
        if payload.get_content_type() == 'text/plain':
            if type(payload.get_payload()) is str:
                return payload.splitlines()
            else:
                return payload.get_payload().splitlines()
               

def renumber(grocery_list):
    return list(enumerate( [grocery_item for (old_index, grocery_item) in grocery_list]))

def remove_items(space_sep_string, grocery_list):
    com, args = space_sep_string.split(" ",1)
    nums = [int(x) for x in args.split(" ")]
    return remove_items_pure(nums, grocery_list)

def remove_items_pure(nums, grocery_list):
    copied_grocery_list = []
    for item in grocery_list:
        if item[0] in nums:
            continue
        else:    
            copied_grocery_list.append(item)
    return copied_grocery_list

def execute(email_line_list, grocery_data):
    INDESTRUCTABLE_OBJECT = -1
    for line in email_line_list:
        line = line.strip()
        if line.startswith(("r ","R ")):
            grocery_data = remove_items(line, grocery_data)
        elif line.startswith(("a ","A ","add ","Add ")):
            line_item = line.split(" ",1)[1]
            grocery_data.append([INDESTRUCTABLE_OBJECT, line_item])
        else:
            continue
    grocery_data = renumber(grocery_data)
    return grocery_data

def write_page(grocery_list):
    page = "<html><body>\n"
    for item in grocery_list:
        page += "<p>"+str(item[0])+": "+str(item[1])+"</p>\n"
    page +="</body></html>"
    return page

def find_email_sender(parsed_email):
    for thing in parsed_email.items():
        if 'Return-Path' in thing:
            return thing[1]
        else:
            return "swartzcr@gmail.com"

def textify_grocery_data(grocery_data):
    text = "The current contents of the grocery list are:\n"
    for row in grocery_data:
        text += str(row[0])+": "+str(row[1])+"\n"
    text += "\n"
    text += "remember to remove items reply with their numbers, space seperated on a line beginning with 'r '\n"
    text += "for example 'r 1 2 3' would remove items 1, 2, and 3\n"
    text += "to add items start each line with an a or add put them on seperate lines of your email\n"
    text += "to check the contents of the list ANY TIME go to rose.makesad.us/~swartzcr/grocery/\n"
    text += "remember to send your replies to swartzcr@rose.makesad.us"
    return text

def send_email(grocery_data, parsed_email):
    email_sender = find_email_sender(parsed_email)
    grocery_data_text = textify_grocery_data(grocery_data)
    me = "swartzcr@gmail.com"
    msg = MIMEText(grocery_data_text)
    msg['Subject']= 'You added items to the grocery list!'
    msg['From'] = me
    msg['To'] = str(email_sender)
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [email_sender], msg.as_string())
    s.quit()

class AutomtedTest(unittest.TestCase):
    dir_name = os.path.dirname(os.path.abspath(__file__))

    def test_parse_email_to_list(self):
        with open(dir_name+"/test.txt") as f:
            test_email = f.read()
        result =  parse_email(test_email)
        self.assertEqual(result, ["hsa","ashd", "ashd"])

    def test_renumber(self):
        result = renumber([[2, 'a'],[1,'b'],[17, 'c']])
        self.assertEqual(result, [(0, 'a'),(1,'b'),(2,'c')])

    def test_remove_items(self):
        result = remove_items("r 2 3", [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4,'e'), (5, 'f')])
        self.assertEquals(result, [(0,'a'), (1,'b'), (4, 'e'), (5, 'f')])

    def test_remove_trailing_whitespace(self):
        result = execute([("r 2 3 ")], [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4,'e'), (5, 'f')])
        self.assertEquals(result, [(0,'a'), (1,'b'), (2, 'e'), (3, 'f')])

    def test_write_website(self):
        result = write_page([(0, 'a'), (1,'b')])
        self.assertEquals()

def main():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    with open(dir_name+"/grocery.json") as js:
        grocery_data = json.load(js)
    email_data = sys.stdin.read()
    parsed_email = parse_email(email_data)
    email_line_list = parsed_email2split_lines(parsed_email)
    grocery_data = execute(email_line_list, grocery_data)
    with open(dir_name+"/grocery.json", 'w') as f:
        json.dump(grocery_data, f)
    page = write_page(grocery_data)
    with open(dir_name+"/index.html",'w') as fi:
        fi.write(page)
    send_email(grocery_data, parsed_email)

if __name__ == "__main__":
    #unittest.main()
    main()        

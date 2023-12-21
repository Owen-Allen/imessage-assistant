#!/usr/bin/python3
import os
import argparse
import sqlite3

DB_PATH = '/Users/owenallen/Library/Messages/chat.db'

class Message:
    def __init__(self, guid, text, date, is_from_me):
        self.guid = guid
        self.text = text
        self.date = date
        self.is_from_me = bool(is_from_me)

    def __str__(self):
        return f'''Message:\n         guid: {self.guid} \n         text: {self.text} \n         date: {self.date} \n   is_from_me: {self.is_from_me}'''
    

def get_recent_message(phone: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f'''select m.guid, m.text, m.date, m.is_from_me
                      from message as m join handle as h on m.handle_id = h.ROWID
                      and h.id = "{phone}"
                      where m.is_from_me = 0
                      order by date desc
                      limit 1;
                   ''')

    results = cursor.fetchall()
    if(len(results)):
        message = Message(*results[0])
        return message
    else:
        print(f"Could not find any messages from {phone}. Do you have the correct phone number?")
        return False



def generate_response(message: Message):
    # some api call
    return "Sure! That sounds awesome"


def send_text(message: str, phone: str):
    # os.system(f"imessage --text {message} --contacts {phone}")
    return

def main():
    # parse phone # from user input
    parser = argparse.ArgumentParser(description='A chat script that responds to texts using Chat GPT')
    parser.add_argument('-phone', nargs='?', help='Specify the name for the chat')
    args = parser.parse_args()
    phone = args.phone
    phone = phone if phone.startswith("+1") else "+1" + phone

    print(phone)

    print(f"Generating a response for recent texts with, {phone}!")
    message = get_recent_message(phone)
    print(message)
    if(not message): return
    response = generate_response(message)

    # check if user it using safe mode?
    send_text(response, phone)




def tester():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("VALID QUERY")
    cursor.execute('''
                 select m.text, h.id
                 from message as m join handle as h on m.handle_id = h.ROWID
                 and h.id = "+19054073037"
                 where m.is_from_me = 0
                 order by date desc
                 limit 1;
                 ''')

    results = cursor.fetchall()
    print(results)
    print()
    print("INVALID QUERY")

    cursor.execute('''
                select m.text, h.id
                from message as m join handle as h on m.handle_id = h.ROWID
                and h.id = "+134582345982348423"
                where m.is_from_me = 0
                order by date desc
                limit 1;
                 ''')

    results = cursor.fetchall()
    print(results)
    print()


if __name__ == "__main__":
    main()
    # tester()
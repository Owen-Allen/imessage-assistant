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
    

def get_phone_number():
    parser = argparse.ArgumentParser(description='A chat script that responds to texts using Chat GPT')
    parser.add_argument('-phone', nargs='?', help='phone number number of person you want to respond to')
    args = parser.parse_args()
    phone_number = args.phone

    if(not phone_number):
        raise Exception("No phone number found in user input. -phone [+12345]")

    phone_number = phone_number if phone_number.startswith("+1") else "+1" + phone_number
    return phone_number

def get_recent_incoming_message(phone_number: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f'''select m.guid, m.text, m.date, m.is_from_me
                      from message as m join handle as h on m.handle_id = h.ROWID
                      and h.id = "{phone_number}"
                      where m.is_from_me = 0
                      order by date desc
                      limit 1;
                   ''')

    results = cursor.fetchall()
    if(len(results)):
        message = Message(*results[0])
        return message
    else:
        raise Exception(f"No message found from {phone_number}")

def generate_message_response(message: Message):
    # some api call
    return "Sure! That sounds awesome"
.py

def send_text(message: str, phone_number: str):
    os.system(f"imessage --text '{message}' --contacts {phone_number}")
    return

def main():
    phone_number = get_phone_number()
    message = get_recent_incoming_message(phone_number)
    message_response = generate_message_response(message)
    send_text(message_response, phone_number)


if __name__ == "__main__":
    main()
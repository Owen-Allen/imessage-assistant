#!/usr/bin/python3
import os
import sqlite3
from .message import Message, MessageList
from .conversation import Conversation
from .cli import ArgParserWrapper


DB_PATH = '/Users/owenallen/Library/Messages/chat.db'

# TO DO
# Ensure texts are from 1 convo only in get query
    # ADD A CONVERSATION ID?
    # when finding the correct conversation id, scrape chat.db and make sure messages always come from the same contact?
    # or select the one with the fewest
    # how does apple sort each conversation?
# how do I make a pretty print for within a list?
# seperate db access into a seperate class
# ConversationManager should just be a conversation, and have some other sort of manager aka main



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
    conn.close()
    if(len(results)):
        message = Message(*results[0])
        return message
    else:
        raise Exception(f"No message found from {phone_number}")

def generate_message_response(message: Message):
    # some api call
    return "Sure! That sounds awesome"

def send_text(message: str, phone_number: str):
    os.system(f"imessage --text '{message}' --contacts {phone_number}")
    return

def main():
    messages = get_recent_incoming_message("+19054073037")


if __name__ == "__main__":
    main()
    a = MessageList()


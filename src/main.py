#!/usr/bin/python3
import os
import sqlite3
from .message import Message, MessageList
from .conversation import Conversation
from .cli import ArgParseWrapper
from .chat import ChatAPI

DB_PATH = '/Users/owenallen/Library/Messages/chat.db'

def generate_message_response(message: Message):
    # some api call
    return "Sure! That sounds awesome"

def send_text(message: str, phone_number: str):
    os.system(f"imessage --text '{message}' --contacts {phone_number}")
    return

def main():
    parser = ArgParseWrapper()
    args = parser.parse_args()

    chat_db = ChatAPI(DB_PATH)

    conversation = Conversation(args.phone, chat_db)
    conversation.refresh_messages()
    return



if __name__ == "__main__":
    main()
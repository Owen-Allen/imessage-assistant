#!/usr/bin/python3
import os
import time
import json
from dotenv import load_dotenv
from openai import OpenAI
import shlex


from .message import Message, MessageList
from .conversation import Conversation
from .cli import ArgParseWrapper
from .chat import ChatAPI


DB_PATH = "/Users/owenallen/Library/Messages/chat.db"


openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)


def send_text(message: str, phone_number: str):
    print("sending text")

    safe_message = message.replace("'", "'\\''")
    print(safe_message)
    os.system(f"imessage --text '{safe_message}' --contacts {phone_number}")
    return

def show_json(obj):
    json_object = json.loads(obj.model_dump_json())
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


def main():
    parser = ArgParseWrapper()
    args = parser.parse_args()

    phone_number = args.phone
    chat_db = ChatAPI(DB_PATH)

    conversation = Conversation(args.phone, chat_db)

    instructions = ""
    with open("instructions", "r") as f:
        instructions = f.read()

    assistant = client.beta.assistants.create(
        name="iMessage Assistant",
        instructions=instructions,
        model="gpt-3.5-turbo"
    )

    thread = client.beta.threads.create()


    # thread created, start feeding messages to assistant
    last_message_id = -1
    while True:
        # prepare message for assistant
        message_from_user = conversation.get_latest_from_user()

        if(message_from_user.guid == last_message_id):
            time.sleep(5)
            continue

        last_message_id = message_from_user.guid

        client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=message_from_user.text,
        )

        # send assistant a message
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        wait_on_run(run, thread)

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        message_to_user = messages.data[0].content[0].text.value
        send_text(message_to_user, phone_number)
        time.sleep(5)
        conversation.refresh_messages()
        # show_json(messages)

    # start a thread
    # create the initial message, which is tied to the thread
    # create a run, by tying the thread to the assistant
    # start loop?


if __name__ == "__main__":
    main()

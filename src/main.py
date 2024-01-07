#!/usr/bin/python3
import os
import time
import logging
from dotenv import load_dotenv
from openai import OpenAI
from .conversation import Conversation
from .cli import ArgParseWrapper
from .chat import ChatAPI

load_dotenv()

DB_PATH = os.getenv('DB_PATH')
OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPEN_AI_KEY)

def send_text(message: str, phone_number: str):
    logging.info("Sending text")
    safe_message = message.replace("'", "'\\''")
    os.system(f"imessage --text '{safe_message}' --contacts {phone_number}")

def wait_on_run(run, thread):
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(0.5)
    return run

def load_instructions(file_path="instructions"):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except IOError:
        logging.error(f"Failed to read instructions from {file_path}")
        return ""

def main():
    logging.basicConfig(level=logging.INFO)
    parser = ArgParseWrapper()
    args = parser.parse_args()
    phone_number = args.phone

    chat_db = ChatAPI(DB_PATH)
    conversation = Conversation(args.phone, chat_db)
    instructions = load_instructions()

    assistant = client.beta.assistants.create(
        name="iMessage Assistant",
        instructions=instructions,
        model="gpt-3.5-turbo"
    )
    thread = client.beta.threads.create()

    last_message_id = -1
    try:
        while True:
            conversation.refresh_messages()
            messages_from_user = conversation.get_messages_after(last_message_id)
            if len(messages_from_user) == 0:
                time.sleep(5)
                continue

            last_message_id = messages_from_user[-1].guid

            combined_message_text = ""
            for message in messages_from_user:
                combined_message_text += message.text + "  "

            client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=combined_message_text,
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )
            wait_on_run(run, thread)

            messages = client.beta.threads.messages.list(thread_id=thread.id)
            message_to_user = messages.data[0].content[0].text.value
            if(message_to_user == "STOP"):
                break
        
            send_text(message_to_user, phone_number)
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

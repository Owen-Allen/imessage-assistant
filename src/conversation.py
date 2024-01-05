from .chat import ChatAPI
from .message import Message, MessageList


class Conversation:

    def __init__(self, phone_number, chat_api):
        self.phone_number = phone_number
        self.chat = chat_api
        self.messages = MessageList()
        self.init_messages()

    def __str__(self):
        return f'''Conversation with {self.phone_number}
                    {self.messages}'''

    def init_messages(self):
        messages = self.chat.get_recent_messages(self.phone_number, 1)
        self.messages = messages

    def refresh_messages(self):
        # check the chat for new messages, if so, update our messages
        latest_message = self.messages[-1]
        new_messages = self.chat.get_messages_since(self.phone_number, latest_message.date)
 
        for message in new_messages:
            self.messages.append(message)
        return
    
    def get_latest_from_user(self):
        for message in reversed(self.messages):
            if not message.is_from_me:
                return message
        raise Exception('No message from user')

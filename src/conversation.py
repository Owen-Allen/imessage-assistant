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
        new_messages = self.chat.get_messages_since(latest_message.date, self.phone_number)
 
        for message in new_messages:
            if not message.is_from_me:
                self.messages.append(message)
    
    def get_messages_after(self, guid) -> MessageList:
        ret_messages = MessageList()
        for message in reversed(self.messages):
            if message.guid == guid:
                break
            if not message.is_from_me:
                ret_messages.append(message)
        return ret_messages

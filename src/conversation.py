from .chat import ChatAPI
from .message import Message, MessageList


class Conversation:
    # TODO add compute id function
    # initialize with most recent text? default 1, maybe users can use have a context flag for how many messages back they sent
    # a conversation should just be a list of messages, but preserves order based on m.date
    def __init__(self, phone_number, chat_api):
        self.phone_number = phone_number
        self.chat = chat_api
        self.index_latest_messaged_recieved = -1
        self.id = 0
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

import unittest
from context import Conversation, Message, MessageList

class MockChatAPI:
    def __init__(self):
        # Predefined messages for testing
        self.predefined_messages = [
            Message("guid1", "Hello, how are you?", 0, False),
            Message("guid2", "I'm good, thanks!", 1, False),
            Message('guid3', 'Message3', 2, False),
            Message('guid4', 'Message4', 3, False)
        ]

    def get_recent_messages(self, phone_number, quantity):
        # Return the last 'quantity' number of messages
        return MessageList(self.predefined_messages[-quantity:])

    def get_messages_since(self, date: int, phone_number):
        # Return messages since a given date
        return MessageList([msg for msg in self.predefined_messages if msg.date > date])







class TestConversation(unittest.TestCase):

    def test_init(self):
        mock_chat = MockChatAPI()
        conversation = Conversation('+17052052944', mock_chat)
        self.assertEqual(conversation.phone_number,'+17052052944')
        self.assertEqual(conversation.messages[0].text, mock_chat.predefined_messages[-1].text)

    def test_refresh_messages(self):
        mock_chat = MockChatAPI()
        conversation = Conversation('+17052052944', mock_chat)
        
        new_message = Message('guid3', 'Message3', 999, False)
        mock_chat.predefined_messages.append(new_message)

        conversation.refresh_messages()
        self.assertTrue(len(conversation.messages), len(mock_chat.predefined_messages))
        self.assertEqual(conversation.messages[-1], new_message)

    def test_get_messages_after(self):
        mock_chat = MockChatAPI()
        conversation = Conversation('+17052052944', mock_chat)
        conversation.messages = MessageList()

        conversation.messages.append(Message("guid1", "Hello, how are you?", 0, False))
        conversation.messages.append(Message("guid2", "I'm good, thanks!", 1, False))
        conversation.messages.append(Message('guid3', 'Message3', 2, False))
        conversation.messages.append(Message('guid4', 'Message4', 3, False))
        
        all_messages = conversation.get_messages_after('guid_not_in_conversation')
        self.assertEqual(len(all_messages), len(mock_chat.predefined_messages))

        latest_2_messages = conversation.get_messages_after('guid2')
        self.assertEqual(len(latest_2_messages), 2)

        no_messages = conversation.get_messages_after('guid4')
        self.assertEqual(len(no_messages), 0)




if __name__ == '__main__':
    unittest.main()
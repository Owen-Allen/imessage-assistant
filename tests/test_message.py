# test_message.py

import unittest
from context import Message, MessageList

class TestMessage(unittest.TestCase):

    def test_message_creation(self):
        msg = Message("123", "Hello", 100000, True)
        self.assertEqual(msg.guid, "123")
        self.assertEqual(msg.text, "Hello")
        self.assertEqual(msg.date, 100000)
        self.assertTrue(msg.is_from_me)

    def test_message_lt(self):
        less = Message("123", "this message is older", 1, True)
        greater = Message("456", "this message is newer", 2, True)
        self.assertTrue(less < greater)


class TestMessageList(unittest.TestCase):

    def test_append_message(self):
        ml = MessageList()
        msg1 = Message("123", "Hello", 1, True)
        msg2 = Message("456", "Hi",    2, False)
        ml.append(msg1)
        ml.append(msg2)
        self.assertEqual(len(ml), 2)
        self.assertIn(msg1, ml)
        self.assertIn(msg2, ml)

    def test_append_non_message(self):
        ml = MessageList()
        with self.assertRaises(TypeError):
            ml.append("not a message")

    def test_ordering(self):
        ml = MessageList()
        msg1 = Message("123", "Hello", 2, True)
        msg2 = Message("456", "Hi",    1, False)
        ml.append(msg1)
        ml.append(msg2)
        self.assertEqual(ml[0], msg2)
        self.assertEqual(ml[1], msg1)

if __name__ == '__main__':
    unittest.main()
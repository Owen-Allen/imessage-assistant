from .message import Message, MessageList

import sqlite3
class Conversation:
    # TODO add compute id function
    # initialize with most recent text? default 1, maybe users can use have a context flag for how many messages back they sent
    # a conversation should just be a list of messages, but preserves order based on m.date
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.messages = MessageList()
        self.index_latest_messaged_recieved = -1
        self.id = 0

    def get_messages_from_db(self, number_of_messages):
        conn = sqlite3.connect('~/Library/Messages/chat.db')
        cursor = conn.cursor()

        cursor.execute(f'''select m.guid, m.text, m.date, m.is_from_me
                        from message as m join handle as h on m.handle_id = h.ROWID
                        and h.id = "{self.phone_number}"
                        where m.is_from_me = 0
                        order by date desc
                        limit {number_of_messages};
                    ''')

        results = cursor.fetchall()

        if(len(results)):
            messages_list = []
            for message in results:
                messages_list.append(Message(*message))

            return messages_list

        else:
            raise Exception(f"No message found from {self.phone_number}")

    def get_latest_messages(self):
        # see if there are any new messages recieved
        # compare the most recent message in messages to the 

        last_recorded_message = self.messages[len(self.messages) - 1]
        new_messages = self.get_messages_from_db(10)

        match_index = -1

        for i in range(0, len(new_messages)):
            message = new_messages[i]
            if(message.guid == last_recorded_message.guid):
                match_index = i
                break
                # we've caught up to our recent, so we need to slice 0 to message_index

        if match_index == -1:
            raise Exception("Could not find a match. Did we recieve a ton of texts?")
        
        messages_to_add = new_messages[0:match_index]

        self.add_messages(messages_to_add)
    
        return


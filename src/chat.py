import sqlite3
from .message import Message, MessageList

DB_PATH = '/Users/owenallen/Library/Messages/chat.db'

class ChatAPI:
    '''
    An API for querying the iMessage chat.db
    '''

    def __init__(self, db_path):
        self.db_path = db_path

    def get_recent_messages(self, phone_number, quantity):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(f'''select m.guid, m.text, m.date, m.is_from_me
                        from message as m join handle as h on m.handle_id = h.ROWID
                        and h.id = "{phone_number}"
                        order by date desc
                        limit {quantity};
                    ''')
        
        results = cursor.fetchall()
        conn.close()
        
        messages = MessageList()
        for result in results:
            message = Message(*result)
            messages.append(message)

        return messages

    def get_messages_since(self, phone_number, date: int):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(f'''SELECT m.guid, m.text, m.date, m.is_from_me
                FROM message AS m JOIN handle AS h ON m.handle_id = h.ROWID
                WHERE h.id = "{phone_number}" AND m.date > {date}
                ORDER BY m.date ASC;
                    ''')
        
        results = cursor.fetchall()
        conn.close()
        
        messages = MessageList()
        for result in results:
            message = Message(*result)
            messages.append(message)

        return messages


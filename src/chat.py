import sqlite3


DB_PATH = '/Users/owenallen/Library/Messages/chat.db'


class ChatAPI:
    '''
    An API for specifiy queries the iMessage chat.db
    '''

    def get_recent_incoming_message(phone_number: int):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(f'''select m.guid, m.text, m.date, m.is_from_me
                        from message as m join handle as h on m.handle_id = h.ROWID
                        and h.id = "{phone_number}"
                        where m.is_from_me = 0
                        order by date desc
                        limit 1;
                    ''')

        results = cursor.fetchall()
        if(len(results)):
            message = Message(*results[0])
            return message
        else:
            raise Exception(f"No message found from {phone_number}")
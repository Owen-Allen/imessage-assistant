class Message:
    """
    Represents a single iMessage. Comparison operators based on date, with equivalence based on guid.
    """
    def __init__(self, guid, text, date, is_from_me):
        self.guid = guid
        self.text = text
        self.date = date
        self.is_from_me = bool(is_from_me)    

    def __str__(self):
        return f'''Message:\n         guid: {self.guid} \n         text: {self.text} \n         date: {self.date} \n   is_from_me: {self.is_from_me}'''

    def __lt__(self, other):
        if isinstance(other, Message):
            return self.date < other.date
        raise NotImplemented

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.guid == other.guid
        return False


class MessageList(list):
    """
    Custom list class for storing Message objects. Ensures that all elements in the list
    are of type Message and maintains the elements in sorted order based on their date.
    """
    def append(self, message):
        # add message and maintain order
        if not isinstance(message, Message):
            raise TypeError("Only Message objects can be added to this list")

        # find correct insert location
        for i, existing_message in enumerate(self):
            if message < existing_message:
                self.insert(i, message)
                break
        else:
            super().append(message)
    
    def __str__(self):
        return "[" + ", \n ".join(str(message) for message in self) + "]"
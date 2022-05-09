class Error:
    @classmethod
    def create_unaddressed(cls, message):
        return cls(chat_id=None, message=message)

    def __init__(self, chat_id, message):
        self.chat_id = chat_id
        self.message = message

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id_setter(value)

    def _chat_id_setter(self, value):
        self._chat_id = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message_setter(value)

    def _message_setter(self, value):
        self._message = value

class RMGroup:
    @classmethod
    def create_empty(cls, id, name):
        return cls(id, name, users=None, chat_id=None)

    @classmethod
    def create_with_users(cls, id, name, users):
        return cls(id, name, users, chat_id=None)

    def __init__(self, id, name, users, chat_id):
        self.id = id
        self.name = name
        self._users = users
        self.chat_id = chat_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name_setter(value)

    def _name_setter(self, value):
        self._name = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id_setter(value)

    def _id_setter(self, value):
        self._id = value

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id_setter(value)

    def _chat_id_setter(self, value):
        self._chat_id = value

    @property
    def users(self):
        return self._users

    def add_users(self, *values):
        if self._users is None:
            self._users = []
        for value in values:
            self._users.append(value)

    def delete_users(self, *values):
        for value in values:
            removal_index = [index for index, name in enumerate(self._users) if name == value]
            for index in reversed(removal_index):
                del self._users[index]

    def __repr__(self):
        return f"{self.name} (users: {self._users})"

    def __str__(self):
        return f"{self.name}: \n"

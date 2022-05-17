class RMGroup:
    @classmethod
    def create_empty(cls, id, name):
        return cls(id, name, users=list(), chat_id=str())

    @classmethod
    def create_with_users(cls, id, name, users):
        return cls(id, name, users, chat_id=str())

    def __init__(self, id: int, name: str, users: list, chat_id: str):
        self.id = id
        self.name = name
        self._users = users
        self.chat_id = chat_id
        self.filtered = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value: str):
        self._chat_id = value

    @property
    def users(self):
        return self._users

    def add_users(self, users: list):
        self._users.extend(users)

    def _get_users_status(self):
        return "".join(
            [user.filtered() if self.filtered else f"{i}) {user}" for i, user in enumerate(self.users, start=1)])

    def __repr__(self):
        return f"{self.name} (users: {self._users})"

    def __str__(self):
        users_status = self._get_users_status()
        return f"<b>{self.name}:</b> \n\n" + (users_status if users_status else "✅ Все заполнено!")

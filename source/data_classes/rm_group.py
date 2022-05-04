class RMGroup:
    @classmethod
    def create_empty(cls, name, rm_id):
        return cls(name, rm_id, users=None)

    @classmethod
    def create_with_users(cls, name, rm_id, users):
        return cls(name, rm_id, users)

    def __init__(self, name, rm_id, users):
        self.name = name
        self.rm_id = rm_id
        self._users = users

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
    def users(self):
        return self._users

    def add_users(self, values):
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

class RMGroup:
    def __init__(self):
        self.name: str
        self.id: int
        self._users = None

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

    @users.setter
    def users(self, value):
        self._add_user(value)

    def _add_user(self, value):
        if self._users is None:
            self._users = []
        self._users.append(value)

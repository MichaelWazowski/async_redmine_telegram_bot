class RMUser:
    def __init__(self):
        self.name: str
        self.id: int
        self.hours: int
        self.comments: int

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
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        self._hours_setter(value)

    def _hours_setter(self, value):
        self._hours = value

    @property
    def comments(self):
        return self.comments

    @comments.setter
    def comments(self, value):
        self._comments_setter(value)

    def _comments_setter(self, value):
        self._comments = value

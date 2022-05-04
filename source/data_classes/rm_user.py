class RMUser:
    @classmethod
    def create(cls, name, id):
        return cls(name, id, hours=0, comments=0)

    def __init__(self, name, id, hours, comments):
        self.name = name
        self.id = id
        self.hours = hours
        self.comments = comments

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

    def __repr__(self):
        return f"{self._name} (id: {self._id}, hours: {self._hours}, comments: {self._comments})"

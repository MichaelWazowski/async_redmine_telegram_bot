class RMUser:
    @classmethod
    def create(cls, id, name):
        return cls(id, name, hours=None, comments=None)

    def __init__(self, id, name, hours, comments):
        self.id = id
        self.name = name
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
        self._hours = value

    @property
    def comments(self):
        return self.comments

    @comments.setter
    def comments(self, value):
        self._comments = value

    def set_time_sheets(self, data):
        if (type(data) is dict) and ("hours" and "comments" in data):
            self.hours = data["hours"]
            self.comments = data["comments"]
        else:
            self.hours = data
            self.comments = data

    def _short_name(self):
        surname, first_name, second_name = self._name.split(" ")
        return f"{surname} {first_name[0]}.{second_name[0]}."

    def __repr__(self):
        return f"\n {self._name} (id: {self._id}, hours: {self._hours}, comments: {self._comments})"

    def __str__(self):
        return f"{self._short_name()} часы: {self._hours}, коментарии: {self._comments} \n"

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

    def set_time_sheets(self, hours, comments):
        self.hours = hours
        self.comments = comments

    def _short_name(self):
        surname, first_name, second_name = self._name.split(" ")
        return f"{surname} {first_name[0]}.{second_name[0]}."

    def __repr__(self):
        return f"\n {self._name} (id: {self._id}, hours: {self._hours}, comments: {self._comments})"

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        component_format_spec = ".1f"
        prefix, dot, suffix = format_spec.partition(".")
        if dot:
            num_decimal_places = int(suffix)
            component_format_spec = f".{num_decimal_places}f"
        hours = format(abs(self.hours), component_format_spec)
        return f"{self._short_name()} часы: {hours}, коментарии: {self._comments} \n"

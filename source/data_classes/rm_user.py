class RMUser:
    @classmethod
    def create(cls, id, name):
        return cls(id, name, hours=int(), comments=int())

    @staticmethod
    def _is_valid(data: dict, keys: list):
        for key in keys:
            if key not in data:
                return False
        return True

    def __init__(self, id: int, name: str, hours: int, comments: int):
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
        self._id = value

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value):
        self._hours_setter(value)

    def _hours_setter(self, value):
        if value >= 0:
            self._hours = value

    @property
    def comments(self):
        return self.comments

    @comments.setter
    def comments(self, value):
        self._comments_setter(value)

    def _comments_setter(self, value):
        if value >= 0:
            self._comments = value

    def set_time_sheets(self, data):
        if self._is_valid(data, ["hours", "comments"]):
            self.hours = data["hours"]
            self.comments = data["comments"]
        else:
            self.hours = data
            self.comments = data

    def filtered(self):
        return filter_time_sheets(self._hours, self._comments, self._short_name())

    def _short_name(self):
        surname, first_name, second_name = self._name.split()
        return f"{surname} {first_name[0]}.{second_name[0]}."

    def __repr__(self):
        return f"\n {self._name} ({self._id=}, {self._hours=}, {self._comments=})"

    def __str__(self):
        return f"{self._short_name()} часы: {self._hours}, коментарии: {self._comments} \n"


def filter_time_sheets(hours, comments, name):
    if comments > 0 and hours > 6.5:
        return str()
    if comments == 0:
        c_text = "коментарии не заполнены;"
        symbol = "&#9999;"
        if hours == 0:
            h_text = "часы не заполнены;"
            symbol = "&#10060;"
        elif 0 < hours < 6.5:
            h_text = "неполные часы;"
            symbol = "&#128337;"
        else:
            h_text = ""
    else:
        c_text = ""
        h_text = "неполные часы;"
        symbol = "&#128337;"
    return f"{symbol} {name}: {h_text} {c_text} \n"

class DataPackage:
    @classmethod
    def create(cls, chat_id: int, ids_list: list, from_date: str, to_date: str or None, filter_status: bool):
        return cls(chat_id, ids_list, from_date, to_date, filter_status)

    def __init__(self, chat_id: int, ids_list: list, from_date: str, to_date: str or None, filter_status: bool):
        self.chat_id = chat_id
        self.ids_list = ids_list
        self.from_date = from_date
        self.to_date = to_date
        self.filter_status = filter_status

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id = value

    @property
    def ids_list(self):
        return self._ids_list

    @ids_list.setter
    def ids_list(self, value):
        self._ids_list = value

    @property
    def from_date(self):
        return self._from_date

    @from_date.setter
    def from_date(self, value):
        self._from_date = value

    @property
    def to_date(self):
        return self._to_date

    @to_date.setter
    def to_date(self, value):
        self._to_date = value

    @property
    def filter_status(self):
        return self._filter_status

    @filter_status.setter
    def filter_status(self, value):
        self._filter_status = value

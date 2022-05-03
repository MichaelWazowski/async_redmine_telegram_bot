class CMLDepartment:
    def __init__(self):
        self.name: str
        self._groups = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name_setter(value)

    def _name_setter(self, value):
        self._name = value

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._add_group(value)

    def _add_group(self, value):
        if self._groups is None:
            self._groups = []
        self._groups.append(value)


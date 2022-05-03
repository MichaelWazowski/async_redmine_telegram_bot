class CMLDepartment:
    @classmethod
    def create_empty(cls, name):
        return cls(name, groups=None)

    @classmethod
    def create_with_groups(cls, name, groups):
        return cls(name, groups)

    def __init__(self, name, groups):
        self.name = name
        self._groups = groups

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

    def __repr__(self):
        return f"{self.name} (groups: {self.groups!r})"

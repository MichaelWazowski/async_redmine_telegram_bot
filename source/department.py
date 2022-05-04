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

    def groups(self):
        return self._groups

    def add_groups(self, value):
        if self._groups is None:
            self._groups = []
        for item in value:
            self._groups.append(item)

    def delete_groups(self, values):
        for value in values:
            removal_index = [index for index, name in enumerate(self._groups) if name == value]
            for index in reversed(removal_index):
                del self._groups[index]

    def __repr__(self):
        return f"{self.name} (groups: {self._groups})"

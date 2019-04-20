from BinaryNumber import Bin


class Register:
    _data = Bin()

    def __init__(self, number):
        self.number = number

    def read_data(self):
        return self._data

    def write_data(self, data):
        self._data = data

    def __repr__(self):
        return f'${self.number}'

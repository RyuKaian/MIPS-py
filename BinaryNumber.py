def convert_to_bin(func):
    def wrapper(*args, **kwargs):
        return Bin(func(*args, **kwargs))
    return wrapper


class Bin:
    def __init__(self, value: object = '', label=''):
        size = 32
        if isinstance(value, str) and value:
            size = len(value)
        elif isinstance(value, int):
            if value < 0:
                value = int(str(Bin(-value).comp()), 2)
            value = bin(value)[2:]

        if len(value) > size:
            value = value[::-1][:size][::-1]

        self.value = value.zfill(size)

    def __str__(self):
        return self.value

    def __int__(self):
        return int(self.value, 2)

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return self.value

    def zfill(self, size):
        return self.value.zfill(size)

    @convert_to_bin
    def __add__(self, other):
        return int(self.value, 2) + int(other.value, 2)

    @convert_to_bin
    def __sub__(self, other):
        return int(self.value, 2) - int(other.value, 2)

    @convert_to_bin
    def __and__(self, other):
        return int(self.value, 2) & int(other.value, 2)

    @convert_to_bin
    def __or__(self, other):
        return int(self.value, 2) | int(other.value, 2)

    @convert_to_bin
    def __xor__(self, other):
        return int(self.value, 2) ^ int(other.value, 2)

    @convert_to_bin
    def not_(self):
        return int(self.value.replace('0', '_').replace('1', '0').replace('_', '1'), 2)

    @convert_to_bin
    def comp(self):
        return int(str(Bin(self.not_()) + Bin(1)), 2)

    @convert_to_bin
    def __lshift__(self, other):
        return (self.value + ''.join(['0' for _ in range(int(other))]))[-len(self.value):]

    @convert_to_bin
    def __rshift__(self, other):
        return (''.join(['0' for _ in range(int(other))]) + self.value)[:len(self.value)]

    @convert_to_bin
    def __lt__(self, other):
        return int(self.value, 2) < int(other.value, 2)

    @convert_to_bin
    def __eq__(self, other):
        if self.value.isnumeric() and other.value.isnumeric():
            return int(self.value, 2) == int(other.value, 2)
        else:
            for v1, v2 in zip(self.value, other.value):
                if v1 == 'x' or v2 == 'x':
                    continue
                if v1 == v2:
                    continue
                return False
            return True

    @convert_to_bin
    def sign_extend(self, amount):
        return ''.join([self.value[0] for _ in range(amount - len(self.value))]) + self.value

    def __setitem__(self, key, value):
        out = list(self.value)
        out[key] = value
        self.value = ''.join(out)

    @convert_to_bin
    def __getitem__(self, item):
        return self.value[::-1][item][::-1]

    def __bool__(self):
        try:
            return bool(int(self.value))
        except ValueError:
            return True

    @convert_to_bin
    def concatenate(self, other):
        return self.value + other.value

    @staticmethod
    @convert_to_bin
    def join(others):
        return ''.join([str(a) for a in others])

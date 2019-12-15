class Computer:
    def __init__(self, code, inputs=None):
        self.code = code.copy()
        self.ptr = 0
        self.relative_base = 0

        if inputs:
            self.inputs = inputs
        else:
            self.inputs = []

    def add_input(self, inp):
        self.inputs.append(inp)

    def get_opcode(self):
        return self.code[self.ptr] % 100

    def get_mode(self, n):
        return self.code[self.ptr] // (10 ** (1 + n)) % 10

    def get_param(self, param_num):
        mode = self.get_mode(param_num)
        index = self.code[self.ptr + param_num]

        if mode == 0:
            return self.read(index)
        elif mode == 1:
            return index
        elif mode == 2:
            return self.read(index + self.relative_base)
        else:
            raise Exception("Invalid mode")

    def set_param(self, param_num, val):
        mode = self.get_mode(param_num)
        index = self.code[self.ptr + param_num]

        if mode == 0:
            self.write(index, val)
        elif mode == 2:
            self.write(index + self.relative_base, val)
        else:
            raise Exception("Invalid mode")

    def read(self, index):
        if index > len(self.code) - 1:
            self.resize(index)

        return self.code[index]

    def write(self, index, val):
        if index > len(self.code) - 1:
            self.resize(index)

        self.code[index] = val

    def resize(self, index):
        self.code += [0 for _ in range(index - len(self.code) + 1)]

    def run(self):
        while self.ptr < len(self.code):
            op = self.get_opcode()
            if op == 99:
                break

            if op == 1:
                self.set_param(3, self.get_param(1) + self.get_param(2))
                self.ptr += 4
            elif op == 2:
                self.set_param(3, self.get_param(1) * self.get_param(2))
                self.ptr += 4
            elif op == 3:
                self.set_param(1, self.inputs.pop())
                self.ptr += 2
            elif op == 4:
                out = self.get_param(1)
                self.ptr += 2
                return out
            elif op == 5:
                self.ptr = self.get_param(2) if self.get_param(1) != 0 else self.ptr + 3
            elif op == 6:
                self.ptr = self.get_param(2) if self.get_param(1) == 0 else self.ptr + 3
            elif op == 7:
                self.set_param(3, int(self.get_param(1) < self.get_param(2)))
                self.ptr += 4
            elif op == 8:
                self.set_param(3, int(self.get_param(1) == self.get_param(2)))
                self.ptr += 4
            elif op == 9:
                self.relative_base += self.get_param(1)
                self.ptr += 2
            else:
                raise Exception("Invalid opcode")
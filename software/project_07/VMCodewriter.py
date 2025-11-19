class VMCodewriter:
    def __init__(self, fileHandle, fileName):
        self.fileHandle = fileHandle
        self.fileName = fileName
        # base addresses locations in RAM
        self.LCL = 1
        self.ARG = 2
        self.THIS = 3
        self.THAT = 4
        # helps to create unique labels
        self.label_count = 0

    # arithmetic commands
    def _add(self) -> str:
        lines = [
            "// add",
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "A=M-1",
            "M=D+M",
        ]
        return "\n".join(lines)

    def _sub(self) -> str:
        lines = [
            "// sub",
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "A=M-1",
            "M=M-D",
        ]
        return "\n".join(lines)

    def _neg(self) -> str:
        lines = [
            "// neg",
            "@SP",
            "A=M-1",
            "M=-M"
        ]
        return "\n".join(lines)

    def _eq(self) -> str:
        label = f"EQUAL_{self.label_count}"
        self.label_count += 1
        lines = [
            "// eq",
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "A=M-1",
            "D=M-D",
            "M=-1",
            f"@{label}",
            "D;JEQ",
            "@SP",
            "A=M-1",
            "M=0",
            f"({label})",
        ]
        return "\n".join(lines)

    def _gt(self) -> str:
        label = f"GREATER_THAN_{self.label_count}"
        self.label_count += 1
        lines = [
            "// gt",
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "A=M-1",
            "D=M-D",
            "M=-1",
            f"@{label}",
            "D;JGT",
            "@SP",
            "A=M-1",
            "M=0",
            f"({label})",
        ]
        return "\n".join(lines)

    def _lt(self) -> str:
        label = f"LESS_THAN_{self.label_count}"
        self.label_count += 1
        lines = [
            "// lt",
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "A=M-1",
            "D=M-D",
            "M=-1",
            f"@{label}",
            "D;JLT",
            "@SP",
            "A=M-1",
            "M=0",
            f"({label})",
        ]
        return "\n".join(lines)

    def _and(self) -> str:
        lines = [
            "// and",
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "A=M-1",
            "M=M&D",
        ]
        return "\n".join(lines)

    def _or(self) -> str:
        lines = [
            "// or",
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "A=M-1",
            "M=M|D",
        ]
        return "\n".join(lines)

    def _not(self) -> str:
        lines = [
            "// not",
            "@SP",
            "A=M-1",
            "M=!M"
        ]
        return "\n".join(lines)

    # memory commands
    def _push_constant(self, const: int) -> str:
        lines = [
            f"// push constant {const}",
            f"@{const}",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _push_pointer(self, arg: int) -> str:
        pointer = self.THIS if not arg else self.THAT
        lines = [
            f"// push pointer {arg}",
            f"@{pointer}",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _pop_pointer(self, arg: int) -> str:
        pointer = self.THIS if not arg else self.THAT
        lines = [
            f"// pop pointer {arg}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{pointer}",
            "M=D"
        ]
        return "\n".join(lines)

    def _push_static(self, index: int) -> str:
        static = self.fileName + '.' + str(index)
        lines = [
            f"// push static {index}",
            f"@{static}",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _pop_static(self, index: int) -> str:
        static = self.fileName + '.' + str(index)
        lines = [
            f"// pop static {index}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{static}",
            "M=D"
        ]
        return "\n".join(lines)

    def _push_temp(self, index: int) -> str:
        addr = 5 + index
        lines = [
            f"// push temp {index}",
            f"@{addr}",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _pop_temp(self, index: int) -> str:
        addr = 5 + index
        lines = [
            f"// pop temp {index}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{addr}",
            "M=D"
        ]
        return "\n".join(lines)

    def _push(self, base_addr: int, index: int) -> str:
        lines = [
            f"// push segment {index}",
            f"@{base_addr}",
            "D=M",
            f"@{index}",
            "D=D+A",
            "A=D",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _pop(self, base_addr: int, index: int) -> str:
        lines = [
            f"// pop segment {index}",
            f"@{base_addr}",
            "D=M",
            f"@{index}",
            "D=D+A",
            "@R13",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
        return "\n".join(lines)

    def writeCode(self, command: list[str]):
        if len(command) == 1:
            cmd = command[0]
            arith_map = {
                'add': self._add,
                'sub': self._sub,
                'neg': self._neg,
                'eq': self._eq,
                'gt': self._gt,
                'lt': self._lt,
                'and': self._and,
                'or': self._or,
                'not': self._not
            }
            if cmd in arith_map:
                self.fileHandle.write(arith_map[cmd]())
        elif len(command) == 3:
            cmd, segment, index = command
            index = int(index)
            if segment in {'local', 'argument', 'this', 'that'}:
                seg_map = {'local': self.LCL, 'argument': self.ARG, 'this': self.THIS, 'that': self.THAT}
                base = seg_map[segment]
                if cmd == 'push':
                    self.fileHandle.write(self._push(base, index))
                elif cmd == 'pop':
                    self.fileHandle.write(self._pop(base, index))
            elif segment == 'temp':
                if cmd == 'push':
                    self.fileHandle.write(self._push_temp(index))
                elif cmd == 'pop':
                    self.fileHandle.write(self._pop_temp(index))
            elif segment == 'static':
                if cmd == 'push':
                    self.fileHandle.write(self._push_static(index))
                elif cmd == 'pop':
                    self.fileHandle.write(self._pop_static(index))
            elif segment == 'pointer':
                if cmd == 'push':
                    self.fileHandle.write(self._push_pointer(index))
                elif cmd == 'pop':
                    self.fileHandle.write(self._pop_pointer(index))
            elif segment == 'constant' and cmd == 'push':
                self.fileHandle.write(self._push_constant(index))

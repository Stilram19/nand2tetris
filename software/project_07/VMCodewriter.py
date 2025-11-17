class VMCodewriter:
    def __init__(self, fileHandle, fileName):
        self.fileHandle = fileHandle
        self.fileName = fileName
        # base addresses locations in RAM
        self.SP = 0
        self.LCL = 1
        self.ARG = 2
        self.THIS = 3
        self.THAT = 4

    # arithmetic commands
    def _add(self) -> str:
    def _sub(self) -> str:
    def _neg() -> str:
    def _eq(self) -> str:
    def _gt(self) -> str:
    def _lt(self) -> str:
    def _and(self) -> str:
    def _or(self) -> str:
    def _not(self) -> str: 

    # memory commands
    def _push_constant(self, const: int) -> str:
        lines = [
            f"// push constant {const}",
            f"@{const}",
            "D=A",
            f"@{self.SP}",
            "A=M",
            "M=D",
            f"@{self.SP}",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _push_pointer(self, arg: int) -> str:
        pointer = self.THIS if not arg else self.THAT
        lines = [
            f"// push pointer {arg}",
            f"@{pointer}",
            "D=M",
            f"@{self.SP}",
            "A=M",
            "M=D",
            f"@{self.SP}",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _pop_pointer(self, arg: int) -> str:
        pointer = self.THIS if not arg else self.THAT
        lines = [
            f"// pop pointer {arg}",
            f"@{self.SP}",
            "M=M-1",
            "A=M",
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
            f"@{self.SP}",
            "A=M",
            "M=D",
            f"@{self.SP}",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _pop_static(self, index: int) -> str:
        static = self.fileName + '.' + str(index)
        lines = [
            f"// pop static {index}",
            f"@{self.SP}",
            "M=M-1",
            "A=M",
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
            f"@{self.SP}",
            "A=M",
            "M=D",
            f"@{self.SP}",
            "M=M+1"
        ]
        return "\n".join(lines)

    def _pop_temp(self, index: int) -> str:
        addr = 5 + index
        lines = [
            f"// pop temp {index}",
            f"@{self.SP}",
            "M=M-1",
            "A=M",
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
            f"@{self.SP}",
            "A=M",
            "M=D",
            f"@{self.SP}",
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
            f"@{self.SP}",
            "M=M-1",
            "A=M",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
        return "\n".join(lines)

    def writeCode(self, command: list[str]):

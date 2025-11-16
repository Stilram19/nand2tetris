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
        self.TEMP = 5

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
    def _pop_pointer(self, arg: int) -> str:
    def _push_static(self, index: int) -> str:
    def _push(self, base_addr: int, index: int) -> str:
    def _pop(self, base_addr: int, index: int) -> str:

    def writeCode(self, command: str[]):

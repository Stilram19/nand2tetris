class Assembler:
    def __init__(self, inputFile: str, outputFile: str):
        # populate symbols with pre-defined symbols in the language specification
        self.symbols = {
           "SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4,
            **{f"R{i}": i for i in range(16)},
            "SCREEN":16384, "KBD":24576
        }

        # file paths
        self.inputFile = inputFile
        self.outputFile = outputFile

        # a c1..c6 for comp in C-instruction
        self.COMP = {
            # a=0
            "0":   "0101010", "1":   "0111111", "-1":  "0111010",
            "D":   "0001100", "A":   "0110000", "!D":  "0001101",
            "!A":  "0110001", "-D":  "0001111", "-A":  "0110011",
            "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
            "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
            "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
            # a=1 (use M instead of A)
            "M":   "1110000", "!M":  "1110001", "-M":  "1110011",
            "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
            "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
            "D|M": "1010101",
        }

        # d1d2d3
        self.DEST = {
            None:  "000", "": "000",
            "M":   "001", "D": "010", "MD": "011",
            "A":   "100", "AM":"101", "AD":"110", "AMD":"111",
        }

        # j1j2j3
        self.JUMP = {
            None:  "000", "": "000",
            "JGT": "001", "JEQ":"010", "JGE":"011",
            "JLT": "100", "JNE":"101", "JLE":"110",
            "JMP": "111",
        }

    # assemble A-instruction
    def _assemble_a(self, value: int) -> str:
        return '0' + format(value, '015b')

    # assemble C-instruction
    def _assemble_c(self, line: str) -> str:
        dest, comp, jump = None, line, None
        if '=' in line:
            dest, comp = line.split('=', 1)
        if ';' in comp:
            comp, jump = comp.split(';', 1)

        comp = comp.replace(' ', '').strip()
        jump = None if jump is None else jump.strip()
        dest_bits = self._dest_bits(dest)

        if comp not in self.COMP:
            raise ValueError(f"Unknown comp: {comp}")
        if jump not in self.JUMP:
            raise ValueError(f"Unknown jump: {jump}")
        return '111' + self.COMP[comp] + dest_bits + self.JUMP[jump]

    def _dest_bits(self, dest: str | None) -> str:
        if not dest:
            return "000"
        d = dest.strip()
        return (
            ('1' if 'A' in d else '0') +
            ('1' if 'D' in d else '0') +
            ('1' if 'M' in d else '0')
        )

    # remove inline comments and surrounding whitespace
    def _clean(self, line: str) -> str:
        return line.split('//', 1)[0].strip()

    # first scan: populate the symbols table with every lable symbol (xxx)
    def firstScan(self) -> None:
        currInstruction = 0
        with open(self.inputFile, "r") as file:
            for line in file:
                # skip comments
                line = self._clean(line)
                if line.startswith('//'):
                    continue
                # skip empty lines
                if not line:
                    continue
                # handle label line
                if line.startswith('(') and line.endswith(')'):
                    label = line[1:-1] # excluding '(' and ')'
                    self.symbols[label] = currInstruction
                else:
                    currInstruction += 1

    # second scan: full assembling 
    def secondScan(self) -> None:
        # to keep track of the current instruction order and the current variable address (starting at 16)
        currVariableAddress = 16

        out = []
        with open(self.inputFile, "r") as file:
            for line in file:
                line = self._clean(line)
                # skip comments
                if line.startswith('//'):
                    continue
                # skip empty lines
                if not line:
                    continue

                # A-instruction handling
                if line.startswith('@'):
                    token = line[1:]
                    if token.isdigit():
                        token = int(token)
                    elif token in self.symbols:
                        token = self.symbols[token]
                    else: # symbol is a variable
                        self.symbols[token] = currVariableAddress 
                        token = currVariableAddress 
                        currVariableAddress += 1
                    out.append(self._assemble_a(token))
                elif line.startswith('('): # is a Label (to skip, already processed in the first scan)
                    continue
                else: # C-instruction handling
                    out.append(self._assemble_c(line))

        # write machine instructions into outFile
        with open(self.outputFile, 'w') as f:
            f.write('\n'.join(out) + '\n')

    # main
    def launch(self):
        self.firstScan()
        self.secondScan()

a = Assembler('test.asm', 'test.hack')
a.launch()

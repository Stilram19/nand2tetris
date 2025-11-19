class VMParser:
    def __init__(self, fileHandle):
        self.fileHandle = fileHandle

    # read the next line, split it into words then return it
    def parseNextLine(self) -> list[str]:
        while True:
            line = self.fileHandle.readline()
            # is it EOF?
            if not line:
                return []
            line = line.strip()
            # if comment or empty, read next line
            if line == "" or line.startswith('//'):
                continue
            line = line.split('//')[0] # remove inline comments if any
            return line.split()

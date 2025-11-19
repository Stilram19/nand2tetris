import os
from VMParser import VMParser
from VMCodewriter import VMCodewriter

class VMTranslator:
    def __init__(self, inFileName: str):
        self.inFileName = inFileName
        base = os.path.splitext(os.path.basename(inFileName))[0]
        self.outFileName = base + '.asm'

    def translate(self):
        with open(self.inFileName, 'r') as inFile, open(self.outFileName, 'w') as outFile:
            parser = VMParser(inFile) 
            codeWriter = VMCodewriter(outFile, os.path.splitext(os.path.basename(self.inFileName))[0])
            currCommand = parser.parseNextLine()
            while currCommand:
                codeWriter.writeCode(currCommand)
                outFile.write("\n")
                currCommand = parser.parseNextLine()

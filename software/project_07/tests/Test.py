import sys
import os

sys.path.append(os.path.abspath(".."))

from VMTranslator import VMTranslator

translator = VMTranslator("StackTest.vm")
translator.translate()


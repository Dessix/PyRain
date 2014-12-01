import hashlib
import os
import math
import itertools
from changeLib import *
from fileLib import *
from domainLib import *
from utilLib import *
from rainLib import *
from pyrain import *
from pathlib import Path


if __name__ == '__main__':
	rtFile = str(input("Please enter the name of your Rainbow Table: "))
	if len(rtFile) == 0:
		p = Path(".")
		rtFiles = list(p.glob("**/*.rt"))
		if len(rtFiles) < 1:
			raise Exception("Must specify a rainbow table, or have one in the current directory")
		rtFile = str(rtFiles[0])
		print("Assuming "+str(rtFile))

	hsh = str(input("Please enter the hash you wish the crack: "))

	print(lookupHash(
		rtFile,
		1000,
		hexToBin(hsh),
		domainDef("a-z", "A-Z", "0-9"),
		lengthMin = int(input("Please input minimum length: ")),
		lengthMax = int(input("Please input maximum length: "))))

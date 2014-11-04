dictFile = "dictionary.txt"
rtFile = "dict.rt"


import hashlib
import os
import math
import itertools
from changeLib import *
from fileLib import *
from domainLib import *
from utilLib import *
from rainLib import *


def generatePasswordsList(outputFile):
	words = set(fileToLines(dictFile))
	sample = random.sample(words, 1000)
	processed = set()
	for word in sample:
		if(random.randint(0, 5) == 0):
			word = word + str(random.randint(0, 99))
		processed.add(word)
	linesToFile(outputFile, processed)

if __name__ == '__main__':
	if not os.path.exists("dict.rt"):
		generateDictRainbowTable(list(fileToLines(dictFile)), rtFile, 1000, domainDef("a-z", "A-Z", "0-9"), chunksize=500, batchExpander=None)
	print(lookupHash(
		rtFile,
		1000,
		hexToBin("e8975f7a50c7140b037a8f8479119149bbe6dbffa0ee88aaaf191e7fc0e5f1c5"),#pervasiveness
		domainDef("a-z", "A-Z", "0-9"),
		lengthMin=3,
		lengthMax=16))


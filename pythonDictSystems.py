dictFile = "dictionary.txt"

import multiprocessing
import functools
import hashlib
import random
import csv
import os
import struct
import base64
import codecs
import math
import itertools
import zmq
from changeLib import *
from fileLib import *
from domainLib import *
from utilLib import *
from rainlib import *


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
		generateDictRainbowTable(list(fileToLines(dictFile)), "dict.rt", 1000, domainDef("a-z", "A-Z", "0-9"), chunksize=500, batchExpander=None)
	print(lookupHash(
		"dict.rt",
		1000,
		hexToBin("e8975f7a50c7140b037a8f8479119149bbe6dbffa0ee88aaaf191e7fc0e5f1c5"),#pervasiveness
		domainDef("a-z", "A-Z", "0-9"),
		lengthMin=3,
		lengthMax=16))


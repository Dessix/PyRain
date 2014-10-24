dictFile = "dictionary.txt"

import concurrent
import concurrent.futures
import hashlib
import random
import csv
import os
import struct
import base64
import codecs
import math
import itertools
from changeLib import *
from fileLib import *
from domainLib import *
from utilLib import *
from baseconv import BaseConverter


def generatePasswordsList(outputFile):
	words = set(fileToLines(dictFile))
	sample = random.sample(words, 1000)
	processed = set()
	for word in sample:
		if(random.randint(0, 5) == 0):
			word = word + str(random.randint(0, 99))
		processed.add(word)
	linesToFile(outputFile, processed)

def generateHashTable(domainGenerator, hashfunc = "sha256"):
	hashbase = hashlib.new(hashfunc)
	for pwd in domainGenerator:
		hashclone = hashbase.copy()
		hashclone.update(pwd.encode())
		hsh = hashclone.digest()
		yield (hsh, pwd)

def numericDomainGenerator(wordgenerator):
	for word in wordgenerator:
		yield word
		for num in range(1, 10):
			yield word + str(num)

def compileHashTable(inputFile, outputFile, generatorModifier = lambda x: x):
	rowsToCsv(outputFile,
		((hsh[0].encode("hex"), hsh[1]) for hsh in
			generateHashTable(
				generatorModifier(
					fileToLines(inputFile)))))

def lookupHash(tableFile, hashValue):
	for row in csvToRows(tableFile):
		if(row[0] == hashValue):
			return row[1]

def sortHashTable(inputFile, outputFile):
	rowsToCsv(outputFile,
		sorted(
			csvToRows(inputFile),
			key=lambda x: x[0]
		)
	)

def writeBinaryHashTable(outputFile, hashPairs):
	with open(outputFile, "wb") as f:
		for hshp in hashPairs:
			writeByteSized(f, hshp[0])
			writeByteSized(f, hshp[1])
			writeByteSized(f, hshp[2])

def reduce(seed, length, domainDistributor):
	return domainDistributor(seed, length)

def computeChain(startPlain, chainLength, domain):
	curr = startPlain
	for i in range(chainLength - 1):
		res = hashlib.sha256(strToBin(curr)).digest()
		curr = domainDistribute(strToBin(str(i)) + res, len(startPlain), domain)
	return hashlib.sha256(strToBin(curr)).digest()

def computeChainLinks(startPlain, chainLength, domain):
	curr = startPlain
	for i in range(chainLength - 1):
		res = hashlib.sha256(strToBin(curr)).digest()
		yield (curr, res)
		curr = domainDistribute(strToBin(str(i)) + res, len(startPlain), domain)
	yield (curr, hashlib.sha256(strToBin(curr)).digest())

#print(("paz", binToBase64(computeChain("pazrawaw", 10000, domainDef("a-z")))))
#printr(domainDistribute(hashlib.sha512(b"0").digest(), 5, domainDef("a-z", "0-9")))

def calculateDictRainbowTableEntry(line, chainLength, domain):
	return (
		strToBin(line),
		hashlib.sha256(strToBin(line)).digest(),
		computeChain(
			line,
			chainLength,
			domain
		)
	)

def calculateDictRainbowTable(inputFile, chainLength, domain):
	allLines = list(fileToLines(inputFile))
	lineCount = len(allLines)
	pointOnePercent = lineCount // 1000
	i = 0
	for line in numericDomainGenerator(allLines):
		i += 1
		if(i/10 % pointOnePercent == 0):
			print("% "+str((i//10)//pointOnePercent/10), line)
		yield calculateDictRainbowTableEntry(line, chainLength, domain)

def generateDictRainbowTable(inputFile, outputFile, chainLength, domain):
	writeBinaryHashTable(outputFile, calculateDictRainbowTable(inputFile, chainLength, domain))

#generateDictRainbowTable(dictFile, "dict.rt", 100, domainDef("a-z", "A-Z", "0-9"))

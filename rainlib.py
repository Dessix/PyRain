
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

def numericDomainGenerator(wordgenerator):
	for word in wordgenerator:
		yield word
		for num in range(1, 10):
			yield word + str(num)

def reduceHash(iteration, seed, length, domain):
	return domainDistribute(strToBin(str(iteration)) + seed, length, domain)

def computeChain(startPlain, chainLength, domain):
	curr = startPlain
	for i in range(chainLength - 1):
		res = hashlib.sha256(strToBin(curr)).digest()
		curr = reduceHash(i, res, len(startPlain), domain)
	return (strToBin(startPlain), hashlib.sha256(strToBin(curr)).digest())

def computeChainLinks(startPlain, chainLength, domain):
	curr = startPlain
	for i in range(chainLength - 1):
		res = hashlib.sha256(strToBin(curr)).digest()
		yield (curr, res)
		curr = reduceHash(i, res, len(startPlain), domain)
	yield (curr, hashlib.sha256(strToBin(curr)).digest())

def calculateDictRainbowTableBatch(line, chainLength, domain, batchExpander = None):
	if batchExpander != None:
		return [calculateDictRainbowTableEntry(l, chainLength, domain) for l in batchExpander(line)]
	else:
		return (calculateDictRainbowTableEntry(line, chainLength, domain),)

def calculateDictRainbowTableEntry(line, chainLength, domain):
	return computeChain(line, chainLength, domain)

def calculateDictRainbowTable(inputLines, chainLength, domain, processes=6, chunksize=1000, batchExpander=numericDomainGenerator):
	allLines = list(inputLines)
	lineCount = len(allLines)
	pointOnePercent = max(lineCount // 1000, 1)
	print("Preparing pool...")
	with multiprocessing.Pool(processes) as p:
		print("Starting pooled operation...")
		i = 0
		for batch in p.imap(functools.partial(calculateDictRainbowTableBatch, chainLength=chainLength, domain=domain, batchExpander=batchExpander), allLines, chunksize=chunksize):
			i += 1
			if(i % pointOnePercent == 0):
				print("% "+str((i//pointOnePercent)/10))
			for entry in batch:
				yield entry
	print("Completed.")

def generateDictRainbowTable(inputLines, outputFile, chainLength, domain, processes=6, chunksize=1000, batchExpander=numericDomainGenerator):
	return writeBinaryHashTable(outputFile, calculateDictRainbowTable(inputLines, chainLength, domain, processes=processes, chunksize=chunksize, batchExpander=batchExpander))

def generateHashCandidateChain(chainNumber, hsh, length, chainLength, domain):
	def internalGenerator(chainNumber, hsh, length, chainLength, domain):
		res = hsh
		for r in range(chainNumber, chainLength):
			curr = reduceHash(r, res, length, domain)
			res = hashlib.sha256(strToBin(curr)).digest()
			yield res
	return list(internalGenerator(chainNumber, hsh, length, chainLength, domain))


def generateHashCandidates(hsh, length, chainLength, domain, processes=6):
	yield hsh
	with multiprocessing.Pool(processes) as p:
		i = 0
		for res in p.imap(functools.partial(generateHashCandidateChain, hsh=hsh, length=length, chainLength=chainLength, domain=domain), range(chainLength), chunksize=math.ceil(chainLength/processes)):
			if(i != 0 and i % 100 == 0):
				print("Iteration: " + str(i) + " of " + str(chainLength))
			i+=1
			for resEntry in res:
				yield resEntry

def generateMultiHashCandidates(hsh, lengthMin, lengthMax, chainLength, domain):
	yield hsh
	for length in range(lengthMin, lengthMax + 1):
		print("Calculating candidates of length " + str(length))
		for candidate in itertools.islice(generateHashCandidates(hsh, length, chainLength, domain), 1, None):
			yield candidate

def lookupMultiHash(tableFile, hsh, domain):
	raise NotImplemented

def lookupHash(tableFile, chainLength, hsh, domain, lengthMin = 1, lengthMax = 16):
	print("Generating candidate set...")
	candidates = set(generateMultiHashCandidates(hsh, lengthMin, lengthMax, chainLength, domain))
	print("Reading chains...")
	chains = readBinaryHashTable(tableFile)
	for chain in chains:
		if chain[1] in candidates:
			rev = reverseHash(chain, chainLength, hsh, domain)
			if(rev != None):
				return rev
	return None

def reverseHash(chain, chainLength, hsh, domain):
	startPlain = binToStr(chain[0])
	links = list(computeChainLinks(startPlain, chainLength, domain))
	if(links[-1][1] != chain[1]):
		raise ValueError("Incorrect chainLength or domain given")
	for link in links:
		if(link[1] == hsh):
			return link[0]
	return None

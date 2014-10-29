
import csv
import struct

def fileToLines(fileName):
	with open(fileName) as f:
		for line in f:
			yield line.strip()

def linesToFile(fileName, lines):
	with open(fileName, "w") as f:
		f.writelines(str(l) + "\n" for l in lines)

def csvToRows(fileName):
	with open(fileName) as f:
		csvr = csv.reader(f, quoting=csv.QUOTE_MINIMAL)
		for row in csvr:
			yield row

def rowsToCsv(fileName, rows):
	with open(fileName, "w", newline='') as f:
		csvw = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
		csvw.writerows(rows)

def writeByte(f, value):
	f.write(struct.pack(">B", value))

def writeByteSized(f, value):
	writeByte(f, len(value))
	f.write(value)

def readByte(f):
	b = f.read(1)
	if(len(b) == 0): return None
	return struct.unpack(">B", b)[0]

def readByteSized(f):
	l = readByte(f)
	if l == None: return None
	return f.read(l)

def writeBinaryHashTable(outputFile, hashPairs):
	with open(outputFile, "wb") as f:
		for hshp in hashPairs:
			writeByteSized(f, hshp[0])
			writeByteSized(f, hshp[1])

def readBinaryHashTable(inputFile):
	with open(inputFile, "rb") as f:
		while True:
			first = readByteSized(f)
			if(first == None):
				break
			second = readByteSized(f)
			if(second == None):
				break
			yield (first, second)

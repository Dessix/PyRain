from changeLib import *
import math

def domainDef(*domParts):
	ret = ""
	for part in domParts:
		if type(part) == str and part[1] == '-':
			ret += "".join(chr(c) for c in range(ord(part[0]), ord(part[2])+1))
		elif type(part) == tuple:
			ret += "".join(chr(c) for c in range(ord(part[0]), ord(part[1])+1))
		else:
			ret += part
	return ret

def binToDomain(bin, domain):
	assert isinstance(bin, bytes)
	curr = 0
	for b in bin:
		curr = curr * 257 + (b + 1)

	domLen = len(domain)
	out = str()
	while curr > 0:
		out += domain[curr % domLen]
		curr //= (domLen)

	assert isinstance(out, str)
	return out

def domainToBin(domInput, domain):
	assert isinstance(domInput, str)
	domLen = len(domain)

	curr = 0
	for c in domInput[::-1]:
		curr = curr * domLen + domain.index(c)

	out = bytearray()
	while curr > 0:
		out.append((curr % 257) - 1)
		curr //= 257

	assert isinstance(out, bytearray)
	return bytes(out[::-1])

def domainDistribute(seed, length, domain):
	encoded = binToDomain(seed, domain)
	res = encoded[:length]
	if(len(res) == length): return res
	return (math.ceil(length / len(encoded)) * encoded)[:length]

testDom = domainDef("a-z", "0-9", "F-R")
testDat = b'\0\0\0412491249060512jmfddkzsdfijwear0[]\0\0\n\0'
assert(domainToBin(binToDomain(testDat, testDom), testDom))

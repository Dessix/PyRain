import codecs

def hexToBin(hex): return codecs.decode(hex, "hex")
def binToHex(bin): return codecs.encode(bin, "hex")
def base64ToBin(b64):
	# b64 = b64.strip()
	# missingPadding = 4 - len(b64) % 4
	# if missingPadding:
	# 	b64 += "=" * missingPadding
	# return codecs.decode(strToBin(b64), "base64")
	return codecs.decode(b64, "base64")
def binToBase64(bin):
	#val = binToStr(codecs.encode(bin, "base64")).replace("\n", "").rstrip("=")
	#return val
	return codecs.encode(bin, "base64")
def binToStr(bin): return codecs.decode(bin, "utf-8")
def strToBin(str): return codecs.encode(str, "utf-8")

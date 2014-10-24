
def printr(*args):
	print(*(repr(arg) for arg in args))

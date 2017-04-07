def sub(lst):
	if not lst:
		return 0
	else:
		return lst[0] + sub(lst[1:])

def mul(lst):
	if not lst:
		return 0
	else:
		return lst[0] + mul(lst[1:])

OPERATORS = {"+": sum, "-": sub, "*": mul}

class nil:
	"""Represents the special empty pair nil in Scheme."""
	def __repr__(self):
		return 'nil'
	def __len__(self):
		return 0
	def __getitem__(self, i):
		raise IndexError('Index out of range')
	def map(self, fn):
		return nil
nil = nil() # this hides the nil class *forever*
class Pair:
	"""Represents the built-in pair data structure in Scheme."""
	def __init__(self, first, second):
		self.first = first
		self.second = second
	def __repr__(self):
		return 'Pair({}, {})'.format(self.first, self.second)
	def __len__(self):
		return 1 + len(self.second)
	def __getitem__(self, i):
		if i == 0:
			return self.first
		return self.second[i-1]
	def map(self, fn):
		return Pair(fn(self.first), self.second.map(fn))


eval = 0
apply = 0
def calc_eval(exp):
	"""Evaluates a Calculator expression represented as a Pair.
	"""
	global OPERATORS
	global eval
	eval += 1
	if isinstance(exp, Pair):
		return calc_apply(calc_eval(exp.first), list(exp.second.map(calc_eval)))
	elif exp in OPERATORS:
		return OPERATORS[exp]
	else: # Primitive expression
		return exp

def calc_apply(op, args):
	"""Applies an operator to a Pair of arguments."""
	global apply
	apply += 1
	return op(args)
print("eval: ", eval, "apply: ", apply)
a = Pair('+', Pair(2, Pair(4, Pair(6, Pair(8, nil)))))
calc_eval(a)
print("eval: ", eval, "apply: ", apply)

eval = 0
apply = 0
print("eval: ", eval, "apply: ", apply)
b = Pair('+', Pair(2, Pair( Pair("*", Pair(4, Pair(Pair("-", Pair(6, Pair(8, nil))), nil))), nil)))
calc_eval(b)
print("eval: ", eval, "apply: ", apply)



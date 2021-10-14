#!/bin/python3
from sympy import *
from os import system
import re


def ppr(x):
	print(pretty(x).replace('»', 'Δ'))

def lpr(x):
	print(latex(x).replace('»', '\Delta '))

def lcp(x):
	s = latex(x).replace("»", "\Delta ")
	system(f'echo "{s}" | xclip -sel clip')

class Sym():
	def __init__(self, short_desc, sym, exact=False):
		self.short_desc = short_desc
		self.s = Symbol(sym)
		self.exact = exact
		if not self.exact:
			self.err = Symbol(f"»{sym}")


class Formula():
	def __init__(self, short_desc, long_desc, formula, sym):
		self.short_desc = short_desc
		self.long_desc = long_desc
		self.s = sym
		for i in self.s:
			exec(f"{str(i.s)}=i.s")
		for i in [j for j in self.s if not j.exact]:
			exec(f"D{str(i.s)}=i.err")
		if type(formula) == type(""):
			exec(f"self.f={formula}")
		else:
			self.f = formula

	def l(self):
		print(latex(self.f))

	def p(self):
		print(self.f)

	def pp(self):
		pprint(self.f)

	def gauss_err(self):
		for i in self.s:
			exec(f"{str(i.s)}=i.s")
		for i in [j for j in self.s if not j.exact]:
			exec(f"D{str(i.s)}=i.err")
		gauss = sqrt(sum([(diff(self.f, i.s)*i.err)**2 for i in self.s if not i.exact]))
		return Formula(f"Gauss error: {self.short_desc}", f"Gauss error: {self.long_desc}", gauss, self.s)

# test
f = Formula('test', 'test formula', "sin(x**2)", [Sym('x', 'x')])
lpr(f.gauss_err().f)

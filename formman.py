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
		lpr(latex(self.f))

	def p(self):
		print(self.f)

	def pp(self):
		ppr(self.f)

	def gauss_err(self):
		for i in self.s:
			exec(f"{str(i.s)}=i.s")
		for i in [j for j in self.s if not j.exact]:
			exec(f"D{str(i.s)}=i.err")
		gauss = sqrt(sum([(diff(self.f, i.s)*i.err)**2 for i in self.s if not i.exact]))
		return Formula(f"Gauss error: {self.short_desc}", f"Gauss error: {self.long_desc}", gauss, self.s)

def gen_form():
	print("Generating Formula")
	form = input("type in formula to generate\n> ")
	p = re.compile(r'[a-zA-Z]+\w*_?\w*')
	pat = set(p.findall(form))
	sym = pat.difference(set(dir()))
	print(f"""reserved constants and funtions:
{pat.symmetric_difference(sym)}
custom constants:
{sym}
""" + '-' * 10)
	s = [Sym(input(f"Short description for {i}\n> "),
		i,
		input(f"is {i} exact (1=True, 0=False, Default=1)\n> ")) for i in list(sym)]
	print('-' * 10)
	short_desc = input("type in a short description or a name for the formula\n> ")
	long_desc = input("type in a detailed description for the formula")
	return Formula(short_desc, long_desc, form, s)

gen_form().p()

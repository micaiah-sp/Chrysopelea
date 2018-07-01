import math
import numpy as np
import matplotlib.pyplot as plt
import io
import subprocess

avl = "/home/micaiah/Avl/bin/avl"

class bb:
	"""
	class for configuring Buzzed Bomber wing.
	ft,slug,s
	"""
	w = 35
	w_span = 2.73
	w_chord = 0.4064
	rho = 0.0023769
	v = 50*5280/3600

	def __init__(self):
		self.scale()

	@property
	def cl(self):
		return self.w/self.q

	@property
	def L(self)

	def plot(self,label=None):
		thetas = np.linspace(0,math.pi/2,100)
		thrust= thetas.copy()
		for n in range(len(thetas)):
			thrust[n] = self.w*math.sin(thetas[n]) + self.w*math.cos(thetas[n])*self.cdi/self.cl
		thetas *= 180/math.pi
		if label:
			plt.plot(thetas,thrust,label=label)
		else:
			plt.plot(thetas,thrust)

	def print(self):
		print("printing parameters")
		print("CL,CDi")
		print(self.cl,self.cdi)
		print("weight")
		print(self.w)
		print()

	@property
	def q(self):
		return 0.5*self.rho*self.v**2

	def scale(self, AR=1,S=1,draw = False):
		self.w_span = bb.w_span * AR**2
		self.w_chord = bb.w_chord* AR**(-0.5)
		self.w = bb.w + self.w_span - bb.w_span + self.w_chord - bb.w_chord

		base = open('baseline.avl')
		text = base.read()
		base.close()
		for y in [41,72]:
			text = text.replace(str(y), str(round(y*AR**0.5,2)))
		for c in [18.3,14]:
			text = text.replace(str(c), str(round(c*AR**-0.5,2)))
		geo = open('ar_test.avl','w')
		geo.write(text)
		geo.close()

		if draw:
			operations = """
g
k
"""
		else:
			operations = ""
		operations += """
a
c {}
x
""".format(self.cl)

		cmd = open('ar_test.ain','w')
		cmd.write("""
load ar_test.avl
oper{}
quit
""".format(operations))
		cmd.close()
		subprocess.run(avl + "<ar_test.ain>ar_test.aot",shell=True)

		perf = open("ar_test.aot")
		perf_text = perf.read()
		perf.close()
		#self.cl = float(perf_text.split("CLtot =")[1].split()[0])
		self.cdi = float(perf_text.split("CDind =")[1].split()[0])

		#self.plot(label="AR *= {}".format(AR) )
		print('AR*={},S*={}'.format(AR,S))
		self.print()

bb8 = bb()
bb8.scale(AR=0.75)
bb8.scale(AR=1.25)

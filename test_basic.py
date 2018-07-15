from chrysopelea import *

s = 'uniform'
#s = 'sin'

for n in [100*m for m in [20]]:
	print("hershey bar")
	line = LiftingLine(n=n,chord='uniform',space=s)
	line.solve(2*math.pi/180)
	line.plot()
	line.print()
	"""
	print("elipse")
	line = LiftingLine(n=n,chord='elipse',space=s)
	line.solve(2*math.pi/180)
	line.plot()
	line.print()
	"""

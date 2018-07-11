from chrysopelea import *

s = 'uniform'

print("hershey bar")
for n in [200*m for m in range(1,4)]:
	line = LiftingLine(n=n,chord='uniform',space=s)
	line.solve(2*math.pi/180)
	print(line.e)
line.plot()
print("elipse")
for n in [100*m for m in range(1,6)]:
	line = LiftingLine(n=n,chord='elipse',space=s)
	line.solve(2*math.pi/180)
	print(line.e)
line.plot()

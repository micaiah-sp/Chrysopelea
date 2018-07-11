from chrysopelea import *

print("hershey bar")
for n in [100*m for m in range(1,11)]:
	line = LiftingLine(n=n,chord='uniform',space='sin')
	line.solve(2*math.pi/180)
	print(line.e)
print("elipse")
for n in [100*m for m in range(10)]:
	line = LiftingLine(n=n,chord='elipse',space='sin')
	line.solve(2*math.pi/180)
	print(line.e)

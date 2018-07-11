from chrysopelea import *

line = LiftingLine(chord='uniform',space='sin')

line.solve(2*math.pi/180)

line.print()
line.plot()

from chrysopelea import *

line = LiftingLine([0.1 for n in range(1999)])
"""
chord = [math.sqrt(1000**2 - (n-1000)**2)/10000 for n in range(2001)]
line = LiftingLine(chord)
print(line.vcoef(0.5,30))
"""

line.solve(2*math.pi/180)

print("cl",line.cl,"cdi",line.cdi)
print("ar",line.ar)
print("e",line.e)
print()
wash = line.upwash[500]
print("wash",wash,'alpha',2*math.pi/180,"cdi/cl",line.cdi/line.cl)
alpha500 = 2*math.pi/180 + wash
print("correct",math.pi*line.chord[500]*alpha500, "actual", line.kappa[500] )

plt.plot(line.kappa)
print(max(abs(line.kappa)))
elip = [-math.sqrt(1000**2 - (n-1000)**2)/1000*max(abs(line.kappa)) for n in range(2001)]
plt.plot(elip)
plt.plot(line.upwash)
plt.show()

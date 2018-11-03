from chrysopelea import *

s = 'uniform'
#s = 'cos'

#c = 'elipse'
c = 'uniform'

lineu = []
linen = []
avle = []
avlform0 = []
avlform1 = []
sw = []

linecl = []
avlcl = []
lineclmax = []

linecd = []
avlcd = []

fact = -1
for sweep in [r/8 for r in range(-40,40)]:

	scale = 10**fact

	sr = Surface("Wing")
	sr.add_naca((0,0,0),scale,nspan=50)
	sr.add_naca((0.5*sweep,0.5,0),scale,nspan=50)
	print(sr.area)
	a = avl()
	a.add_surface(sr)
	a.set_attitude(alpha=5)

	line = LiftingLine(n=2001,chord=c,scale=scale,y=s)
	y,chord = line.r[1],line.chord
	x = sweep*np.abs(y-0.5)
	line = LiftingLine(y=y,chord=chord,x=x)

	line.solve_no_wash(5*math.pi/180)
	lineclmax.append(line.cl)

	line.solve(5*math.pi/180)

	linecl.append(line.cl)
	avlcl.append(a.cl)
	linecd.append(line.cdi)
	avlcd.append(a.cdi)

	lineu.append(line.e)
	linen.append(line.lengthwise_e)
	avle.append(a.e)
	avlform1.append((a.cl**2)/(math.pi*a.ar*(sweep**2+0.5**2)/0.5**2*a.cdi))
	sw.append(sweep)
	print(sweep)

"""
plt.plot(sw,lineu,label='Lifting Line Span')
plt.plot(sw,linen,label='Lifting Line Length')
plt.plot(sw,avle,label='e')
plt.plot(sw,avlform1,label='Cl^2/(pi*l^2/S*Cdi); l = arc length of wing')
plt.ylabel('e')
"""
plt.plot(sw,linecl,label='Lifting Line')
plt.plot(sw,lineclmax,label='Lifting Line limit')
plt.plot(sw,avlcl,label='AVL')
plt.ylabel('C_L')
plt.xlabel('Sweep (defined by length ratio)')
plt.legend()
plt.title('Constant Chord, AR=10')
plt.show()



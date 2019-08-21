from chrysopelea import *

span = 60
chord = 30
vertex = 3

class avl1(avl):
	@property
	def area(self):
		return span*chord
wing_chord = 10

cla = []
sep = []
for separation in range(20):
	separation *= 2
	sheet = Surface('Wing')
	sects = 4
	for n in range(sects+1):
		#sheet.add_naca(  ( vertex*(1-(n/sects)**2), span*n/(2*sects), separation ), (chord-2*vertex*(1-(n/sects)**2))*0.714922  )
		sheet.add_naca(  ( vertex*(1-(n/sects)**2), span*n/(2*sects), separation ), (chord-2*vertex*(1-(n/sects)**2))  )
	
	wing = Surface('aux')
	wing.add_naca((0,0,0),wing_chord)
	wing.add_naca((0,span/2,0),wing_chord)
	#wing.set_nspan(20)
	
	fl = avl1()
	fl.add_surface(sheet)
	fl.add_surface(wing)
	#fl.set_nchord(10)
	#fl.draw()
	
	cl = []
	alpha = [-10,10]
	for a in alpha:
		fl.set_attitude(alpha=a)
		cl.append(fl.cl)
	cla.append((cl[1]-cl[0])/(alpha[1]-alpha[0])*180/math.pi)
	sep.append(separation)
plt.scatter(sep,cla)
plt.xlabel('Separation distance [cm]')
plt.ylabel('Lift Curve Slope')
plt.show()

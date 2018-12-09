from chrysopelea import *

side = 20.5

h = side*math.sqrt(3)/2
cs_start = 4

def make_aircraft(cs_len):
	s = Surface('Wing')
	n = naca(position=(0,0,0),chord=h+cs_len)
	s.add_section(n)

	n = naca(position=(cs_start*math.sqrt(3),cs_start,0), chord = (side/2-cs_start)*math.sqrt(3)+cs_len)
	n.add_control(Control('elevon',xhinge=cs_len/((side/2-cs_start)*math.sqrt(3)+cs_len) ))
	s.add_section(n)

	n = naca(position=(h,side/2,0),chord=cs_len)
	n.add_control(Control('elevon',xhinge=1))
	s.add_section(n)
	s.set_nchord(5)
	s.set_nspan(5)

	a = avl()
	a.xyzref = (0, 0, 0)
	a.add_surface(s)
	return a

cs_len = 2.5
a = make_aircraft(cs_len)

a.draw()
a.set_attitude(alpha=0)
print('xac',a.xac)
print('area',a.area)
print('cs_len',cs_len)
a.xyzref=(a.xac-1,0,0)
a.set_attitude(alpha=10)
con = a.control_variables()['elevon']
a.set(con,'pm 0')
print('cl',a.cl)
print('deflection',a.get_output('elevon'))

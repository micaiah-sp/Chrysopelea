from chrysopelea import *

side = 19.067

h = side*math.sqrt(3)/2
"""
side = 40
h = 15
"""

def make_aircraft(cs_len):
	s = Surface('Wing')
	n = naca(position=(0,0,0),chord=h+cs_len)
	n.add_control(Control('elevon',xhinge=cs_len/(h+cs_len)))
	s.add_section(n)
	n = naca(position=(h,side/2,0),chord=cs_len)
	n.add_control(Control('elevon',xhinge=1))
	s.add_section(n)
	a = avl()
	a.xyzref = (0, 0, 0)
	a.add_surface(s)
	a.set_nchord(20)
	a.set_nspan(20)
	return a

a = make_aircraft(2)
a.xyzref = (10,0,0)
#a.xyzref = (8.3,0,0)

a.draw()
a.set_attitude(alpha=10)
con = a.control_variables()['elevon']
a.set(con,'pm 0')
print('e',a.e)
print('cl',a.cl)
print('cdi',a.cdi)
print('cl/cdi',a.cl/a.cdi)
print('deflection',a.get_output('elevon'))
"""
print(a.cma)
print(a.xac)
"""

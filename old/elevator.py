from chrysopelea import *

s = Surface('Wing')

n = naca(position=(0,0,0),chord=1)
n.add_control(Control('elevator',xhinge = 0.2))
s.add_section(n)

n = naca(position=(0,1,0),chord=1)
n.add_control(Control('elevator',xhinge = 0.2))
s.add_section(n)

a = avl()
a.add_surface(s)
a.set_nspan(10)
a.set_nchord(10)

a.draw()
a.set_attitude(alpha=5)
d = a.control_variables()['elevator']
a.set(d,'pm 0')
print(a.cl,a.cdi)
print(a.get_output('elevator'))

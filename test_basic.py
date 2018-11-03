from chrysopelea import *

s = Surface('Wing')
s.add_naca((0,0,0),1)
s.add_naca((0,1,0),1)
t = Surface('Tail')
n = naca(position=[2,0,0])
c = Control('elevator',xhinge=0.1)
n.add_control(c)
t.add_section(n)
m = naca(position=[2,1,0])
d = Control('elevator',xhinge=0.1)
m.add_control(d)
t.add_section(m)
a = avl()
a.add_surface(s)
a.add_surface(t)

a.set_attitude(alpha=5)
d = a.control_variables()['elevator']
a.set(d,'pm 0')
print(a.cl,a.cdi)
print(a.get_output('elevator'))

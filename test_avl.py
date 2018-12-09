from interface import *

a = avl()
s = Surface('Wing')
s.add_naca((0,0,0),chord=1)
s.add_naca((0,1,0),chord=1)
a.add_surface(s)

a.set_attitude(0)
print(a.cla)

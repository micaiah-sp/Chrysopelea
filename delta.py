from chrysopelea import *

side = 19.067
cs_len = 10

h = side*math.sqrt(3)/2

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

a.draw()
a.set_attitude(alpha=0)
print(a.cl)
print(a.cma)
print(a.xac)
print(a.xac/(h+cs_len))

"""
a.xyzref = (a.xac-0.1*(side+cs_len),0,0)
print('again')
a.set_attitude(alpha=0)
print(a.cl)
print(a.cma)

print('again')
a.set_attitude(alpha=10)
print(a.cl)
print(a.cma)
"""

print('again')
a.set('a','a 10')
c = a.control_variables()['elevon']
a.set(c,'pm 0')
a.execute()
print(a.cl)

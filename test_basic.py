from chrysopelea import *

foo = avl()
s = Surface('Wing')
s.yduplicate = None
s.add_section([0,-5,0],1)
s.add_section([0,5,0],1)
for sec in s.sections:
	sec.nspan = 40
	sec.sspace = 1
s.nchord = 20
foo.add_surface(s)
print(foo)
print(foo.ar)
foo.draw()
foo.set_attitude(alpha=-10)
print(foo.e)
print(foo.cdi)
print((foo.cl**2)/(math.pi*foo.ar*foo.e))
"""
s.add_section([0,0,0],1)
s.add_section([0,0.5,0],1)
foo.add_surface(s)
foo.speed = 50*5280/3600
for sec in s.sections:
	print(sec.re)
print(foo.cd0)
"""

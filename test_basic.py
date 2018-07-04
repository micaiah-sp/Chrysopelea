from chrysopelea import *

foo = imperial_dynamic()
s = Surface('Wing')
s.add_section([0,0,0],1,afile="nlf0215f-il.dat")
s.add_section([0,0.5,0],1,afile="nlf0215f-il.dat")
"""
s.add_section([0,0,0],1)
s.add_section([0,0.5,0],1)
"""
foo.add_surface(s)
foo.speed = 50*5280/3600

print(foo.surfaces["Wing"].sections[0].re)
print(foo.cd0)

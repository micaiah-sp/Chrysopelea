from chrysopelea import *

foo = dynamic()
s = Surface('Wing')
s.add_section([0,0,0],1,afile="nlf0215f-il.dat")
s.add_section([0,0.5,0],3)
foo.add_surface(s)
print(foo.cd0)

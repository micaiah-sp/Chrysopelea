from chrysopelea import *

s = Surface('Wing')
s.add_naca((0,0,0),1)
s.add_naca((0,1,0),1)
print(s.integrated_cd0)
t = Surface('v')
t.add_naca((0,0,0),1)
t.add_naca((0,0,1),1)
t.yduplicate = None
print(t.integrated_cd0)
a = dynamic()
a.add_surface(s)
a.add_surface(t)
print(a.cd0)

from chrysopelea import *

p = avl()

m = Surface('Wing')
m.add_naca((0,0,0),1)
m.add_naca((1,2,0),0.25)
p.add_surface(m)


p.draw()
p.set_attitude(alpha=10)
print(p.cl,p.cdi,p.cl/p.cdi)
1/0

q = avl()

m = Surface('Wing')
m.add_naca((0,0,0),1)
m.add_naca((1,2,0),0.25)
q.add_surface(m)

h = 0.5
bfrac = 1

v = Surface('vertical')
v.add_naca((0,0,0),1)
v.add_naca((0,0,-h),1)
v.yduplicate=None
q.add_surface(v)

s = Surface('sheet')
s.add_naca((0,0,-h),1)
s.add_naca((bfrac,2*bfrac,0),1-0.75*bfrac)
q.add_surface(s)

q.draw()
q.set_attitude(alpha=10)
print(q.cl,q.cdi,q.cl/q.cdi)

print(q.cl/p.cl)
cd0 = 0.005
dp = (p.cdi+cd0)/(p.cl*math.sqrt(p.cl**2+(p.cdi+cd0)**2))
dq = (q.cdi+cd0)/(q.cl*math.sqrt(q.cl**2+(q.cdi+cd0)**2))
print(dp,dq,dp/dq)

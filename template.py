from chrysopelea import *

p = avl()

m = Surface('Wing')
m.add_naca((0,0,0),1)
n = naca(position=(0.5,1,0),chord=0.25+0.75/2)
n.add_control(Control('elevon',xhinge=0.3))
m.add_section(n)
n = naca(position=(1,2,0),chord=0.25)
n.add_control(Control('elevon',xhinge=0.3))
m.add_section(n)
p.add_surface(m)
m.add_naca((1.1, 2, 0.3), 0.2)


p.draw()
p.set_attitude(alpha=10)
print(p.CL,p.CDi,p.CL/p.CDi)
print(p.Cl_beta, p.Cm_alpha, p.Cn_beta)

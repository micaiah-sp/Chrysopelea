from chrysopelea import *

p = avl()

m = Surface('Wing')
m.add_naca((0,0,0),1)
n = naca(position=(0.5,1,0),chord=0.25+0.75/2)
n.add_control(Control('elevon',xhinge=0.3, signdup=-1))
m.add_section(n)
n = naca(position=(1,2,0),chord=0.25)
n.add_control(Control('elevon',xhinge=0.3, signdup=-1))
m.add_section(n)
#m.add_naca((1.1, 2, 0.3), 0.2)
p.add_surface(m)


print(p.mean_aerodynamic_chord)
p.draw()
p.set_attitude(alpha=5)
p.compute_force_dist = True
con = p.control_variables()['elevon']
p.set(con, '{} -5'.format(con))
print(p.CL,p.CDi,p.CL/p.CDi)
print(p.Cl, p.Cm, p.Cn)
#print(p.Cl_beta, p.Cm_alpha, p.Cn_beta)
print(p.compute_Cl('Wing'))
print(p.compute_Cn('Wing'))

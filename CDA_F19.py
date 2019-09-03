from chrysopelea import *

side_len = 1.57*10
le=3.5
te=2.5
cs_dy = 7
cs_dx = 2.5
sweep_cs = False
vstab_max_chord = 3
vstab_taper = 0.7
vstab_sweep = 40
vstab_dz = 3.5
V = 30

discon_dy = 0.01

a = avl()

s = Surface('Wing')
s.add_naca((0,0,0),side_len*np.sqrt(3)/2 + le + te)

s.add_naca((side_len*np.sqrt(3)/2, side_len/2, 0), le + te)

n = naca(position=(side_len*np.sqrt(3)/2 + le, side_len/2 + discon_dy, 0), chord=cs_dx)
n.add_control(Control('elevon', xhinge=0))
s.add_section(n)

if sweep_cs:
    dy = cs_dy/2
    dx = cs_dy * 3/4
else:
    dy = cs_dy
    dx = 0
n = naca(position=(side_len*np.sqrt(3)/2 + le + sweep_cs * dx,
                side_len/2 + dy, 0), chord=cs_dx)
n.add_control(Control('elevon', xhinge=0))
s.add_section(n)

a.add_surface(s)

v = Surface('Vstab')
v.add_naca((le + side_len*np.sqrt(3)/2 + te - vstab_max_chord, side_len/2, 0),\
           chord=vstab_max_chord)
v.add_naca((le + side_len*np.sqrt(3)/2 + te - vstab_max_chord +
                vstab_dz*np.tan(vstab_sweep*np.pi/180), side_len/2, vstab_dz),\
           chord=vstab_max_chord*vstab_taper)
a.add_surface(v)


a.set_nspan(5)
a.set_nchord(10)
#

a.draw()
print('area',a.area)
a.set_attitude(alpha=0)
print('xac',a.xac)
a.xyzref = (a.xac-0.1*(le+te+side_len*np.sqrt(3)/2),0,0)
print('xcg',a.xyzref[0])

S = a.area/144
rho = imperial_dynamic.rho
print(rho)
L = 9/16
CL_req = L/(0.5*rho*V**2*S)

#a.set_attitude(alpha=5)
a.set_attitude(cl=CL_req)
con = a.control_variables()['elevon']
a.set(con, "pm 0")
print('CL',a.CL)
print('alpha', a.alpha)
print('CDi',a.CDi)
print('CL/CDi',a.CL/a.CDi)
print('def',a.get_output('elevon'))
print('CnB',a.Cn_beta)

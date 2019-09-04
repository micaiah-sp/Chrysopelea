from chrysopelea import *

V = 30
nC = 8
tipLen = 9

hlist = []
cllist = []
back = 1.57*nC + tipLen*2
cs_start = back/2 - tipLen
cs_len = 2.5
web = 4

vstab_max_chord = 3
vstab_taper = 0.7
vstab_sweep = 30
vstab_dz = 3.5

#for h in np.linspace(2, 5, 10):
for h in [3]:
    a = avl()
    front = 20-2/math.sqrt(3)*h
    nose = 20*math.sqrt(3)/2 - h
    print('h',h)
#    
    s = Surface('Wing')
    n = naca(position=(0,0,0),chord=nose+h+web)
    s.add_section(n)
    m = naca()

    if cs_start-front/2 < -1:
    	m = naca(position=(cs_start*math.sqrt(3),cs_start-0.1,0),chord=nose+h+web-cs_start*math.sqrt(3))
    	s.add_section(m)
    	n = naca(position=(cs_start*math.sqrt(3),cs_start,0),chord=nose+h+cs_len-cs_start*math.sqrt(3))
    	n.add_control(Control('elevon',xhinge=cs_len/(nose+h+cs_len-cs_start*math.sqrt(3)) ))
    	s.add_section(n)
    	n = naca(position=(nose,front/2,0),chord=h+cs_len)
    elif -1 <= cs_start-front/2 <= 1:
    	n = naca(position=(nose,front/2-0.1,0),chord=h+web)
    	s.add_section(n)
    	n = naca(position=(nose,front/2,0),chord=h+cs_len)
    else:
    	n = naca(position=(nose,front/2,0),chord=h+web)

    if cs_start-front/2 <= 1:
    	n.add_control(Control('elevon',xhinge=cs_len/(h+cs_len)))
    s.add_section(n)

    if cs_start-front/2 > 1:
    	m = naca(position=(nose+(cs_start-front/2)*h*2/front,cs_start-0.1,0),chord=h*(back/2-cs_start)/(back/2-front/2)+web)
    	s.add_section(m)
    	n = naca(position=(nose+(cs_start-front/2)*h*2/front,cs_start,0),chord=h*(back/2-cs_start)/(back/2-front/2)+cs_len)
    	n.add_control(Control('elevon',xhinge=cs_len/(h*(back/2-cs_start)/(back/2-front/2)+cs_len)))
    	s.add_section(n)

    n = naca(position=(nose+h,back/2,0),chord=cs_len)
    n.add_control(Control('elevon',xhinge=1))
    s.add_section(n)

    v = Surface('Vstab')
    v.add_naca((nose+h+web-vstab_max_chord, cs_start, 0),\
               chord=vstab_max_chord)
    v.add_naca((nose+h+web - vstab_max_chord +
                    vstab_dz*np.tan(vstab_sweep*np.pi/180), cs_start, vstab_dz),\
               chord=vstab_max_chord*vstab_taper)
    a.add_surface(v)

    a.xyzref = (0, 0, 0)
    a.add_surface(s)

    a.set_nspan(10)
    a.set_nchord(20)
    m.nspan = 1
#

    a.draw()
    print('area',a.area)
    print('cs_start',cs_start)
    print('cs_len',cs_len)
    a.set_attitude(alpha=0)
    print('xac',a.xac)
    a.xyzref = (a.xac-0.1*(h+nose),0,0)
    print('xcg',a.xyzref[0])

    """
    S = a.area/144
    rho = imperial_dynamic.rho
    L = 9/16
    CL_req = L/(0.5*rho*V**2*S)
    """

    a.set_attitude(alpha=8)
    #a.set_attitude(cl = CL_req)
    con = a.control_variables()['elevon']
    a.set(con,'pm 0')
    print('cl',a.CL)
    print('alpha', a.alpha)
    print('cdi',a.CDi)
    print('cl/cdi',a.CL/a.CDi)
    print('def',a.get_output('elevon'))
    print('Cnb',a.Cn_beta)
    cllist.append(a.CL)
    hlist.append(h)
    print("")
plt.plot(hlist,cllist)
plt.xlabel('h')
plt.ylabel('cl')
#plt.show()

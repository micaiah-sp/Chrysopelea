from chrysopelea import *

#for angle_y in [4, 5, 6, 7]:
for angle_y in [7]:
    nC = 10
    #angle_y = 6
    tip_len = 7
    nspan = 10
    cs_len = 2.5
    dy = 0.01

    vstab_max_chord = 3
    vstab_taper = 0.5
    vstab_sweep = 40
    vstab_dz = 3.5
    vstab_overhang = 1

    side = 1.57*nC
    payload_len = side*math.sqrt(3)/2
    fairing = 4
    max_chord = payload_len + fairing
    angle_x = angle_y*math.sqrt(3)
    span = side + 2*tip_len

    cda = avl()
    wing = Surface("Wing")

    n = naca(position=(0, 0, 0), chord=max_chord, nspan=nspan)
    wing.add_section(n)

    n = naca(position=(angle_x, angle_y, 0), chord=max_chord- angle_x, nspan=nspan)
    wing.add_section(n)

    delta_x = (payload_len - angle_x)*tip_len/(span/2 - angle_y)
    n = naca(position=(payload_len - delta_x, side/2, 0), chord=delta_x + fairing, nspan=1)
    wing.add_section(n)

    delta_x = (payload_len - angle_x)*(tip_len - dy)/(span/2 - angle_y)
    n = naca(position=(payload_len - delta_x, side/2 + dy, 0),\
                       chord=delta_x + cs_len, nspan=nspan)
    n.add_control(Control('elevon', xhinge=cs_len/(delta_x + cs_len)))
    wing.add_section(n)

    n = naca(position=(payload_len, side/2 + tip_len, 0), chord=cs_len, nspan=nspan)
    n.add_control(Control('elevon', xhinge=1))
    wing.add_section(n)

    v = Surface('Vstab')
    v.add_naca((max_chord - vstab_max_chord + vstab_overhang, side/2, 0),\
               chord=vstab_max_chord)
    v.add_naca((max_chord - vstab_max_chord + vstab_overhang +\
                    vstab_dz*np.tan(vstab_sweep*np.pi/180), side/2, vstab_dz),\
               chord=vstab_max_chord*vstab_taper)
    cda.add_surface(v)


    cda.add_surface(wing)
    cda.set_nchord(20)

    cda.draw()
    cda.set_attitude(alpha=0)
    print("Span: {}".format(span))
    print("angle y: {}".format(angle_y))
    print('xac: {}'.format(cda.xac))
    cda.xyzref = (cda.xac-0.5,0,0)
    print('xcg: {}'.format(cda.xyzref[0]))

    cda.set_attitude(alpha=10)
    con = cda.control_variables()['elevon']
    cda.set(con, "pm 0")
    print("CL: {}".format(cda.CL))
    print("CDi: {}".format(cda.CDi))
    print("CL/CDi: {}".format(cda.CL/cda.CDi))
    print("def: {}".format(cda.get_output('elevon')))
    print("CnB: {}".format(cda.Cn_beta))

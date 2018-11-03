from chrysopelea import *

back = 25
h = 15
front = 5

hlist = []
cllist = []
back = 30
cs_start = 1
cs_len = 2
for h in [4.8]:
	front = 20-2/math.sqrt(3)*h
	nose = 20*math.sqrt(3)/2 - h
	print('h',h)
#	
	s = Surface('Wing')
	n = naca(position=(0,0,0),chord=nose+h+cs_len)
	s.add_section(n)

	if cs_start-front/2 < -1:
		n = naca(position=(cs_start*math.sqrt(3),cs_start,0),chord=nose+h+cs_len-cs_start*math.sqrt(3))
		n.add_control(Control('elevon',xhinge=cs_len/(nose+h+cs_len-cs_start*math.sqrt(3)) ))
		s.add_section(n)

	n = naca(position=(nose,front/2,0),chord=h+cs_len)
	n.add_control(Control('elevon',xhinge=cs_len/(h+cs_len)))
	s.add_section(n)

	if cs_start-front/2 > 1:
		n = naca(position=(nose+(cs_start-front/2)*h*2/front,cs_start,0),chord=h*(back/2-cs_start)/(back/2-front/2)+cs_len)
		n.add_control(Control('elevon',xhinge=cs_len/(h*(back/2-cs_start)/(back/2-front/2)+cs_len)))
		s.add_section(n)

	n = naca(position=(nose+h,back/2,0),chord=cs_len)
	n.add_control(Control('elevon',xhinge=1))
	s.add_section(n)

	"""
	t = Surface('vstab')
	c = 1.5
	n = naca(position=(nose+h-c,10,0),chord=c)
	s.add_section(n)
	n = naca(position=(nose+h-c+1,10,2),chord=c)
	s.add_section(n)
	"""

	a = avl()
	a.xyzref = (0, 0, 0)
	a.add_surface(s)
	a.set_nspan(10)
	a.set_nchord(20)
#

	a.draw()
	print('area',a.area)
	print('cs_start',cs_start)
	print('cs_len',cs_len)
	a.set_attitude(alpha=0)
	print('xac',a.xac)
	a.xyzref = (a.xac-1,0,0)

	a.set_attitude(alpha=10)
	con = a.control_variables()['elevon']
	a.set(con,'pm 0')
	print('cl',a.cl)
	print('def',a.get_output('elevon'))
	"""
	print('cnb',a.cnb)
	cllist.append(a.cl)
	hlist.append(h)
	"""
plt.plot(hlist,cllist)
plt.xlabel('h')
plt.ylabel('cl')
#plt.show()

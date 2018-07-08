from chrysopelea import *

bb8 = avl('BB7.avl')
bb8.pop('VerTail')
bb8.pop('HTail')
bb8.draw()
#bb8.set_nchord(50)
#bb8.set_nspan(100)

#for a in np.linspace(-5,10,100):
for a in [3,4,5]:
	bb8.set_attitude(alpha=a)
	print(bb8.cdi)
	print(bb8.cl)
	print(bb8.ar)
	print(bb8.e)
	try:
		num = bb8.cdi
		form = (bb8.cl**2)/(math.pi*bb8.ar*bb8.e)
		print(num,form)
		print(abs(num-form)/num)
	except:
		print('failed')
	print()
	print()

"""
bb9 = imperial_dynamic('BB7.avl')
bb9.pop('VerTail')
bb9.pop('HTail')

def fps(mph):
	return mph*5280/3600

jett_fire46 = motor()
jett_fire46.max = fps(50)
jett_fire46.static_thrust = 11.6
jett_fire46.thrust_at_max = 8.3

bb9.weight = 37
bb9.rho = 0.0023769
bb9.scale(1/12)
bb9.extra_drag = 0.0049*bb9.area
bb9.motor = jett_fire46

bb9.phi_limits = (0,0.3)
bb9.mesh_size = 1
bb9.side_points = 100
print(bb9.max_climb_rate)
bb9.plot_mem()

foo = fast_avl('BB7.avl')
foo.pop('VerTail')
foo.pop('HTail')

print(foo.set_attitude(alpha = 0.2))
print('done')
print(foo.set_attitude(cl=-0.44))
print(foo.set_attitude(cl=-0.34))
print(foo.set_attitude(cl=0.4))
foo.plot_mem()
"""

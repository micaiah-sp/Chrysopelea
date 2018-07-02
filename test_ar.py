from chrysopelea import *

"""
bb9 = dynamic('BB7.avl')
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
print(bb9.max_climb_rate)
"""
foo = fast_avl('BB7.avl')
foo.pop('Vertail')
foo.pop('Htail')
foo.reset()

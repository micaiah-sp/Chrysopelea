from chrysopelea import *

bb9 = dynamic('BB7.avl')
bb9.pop('VerTail')
bb9.pop('HTail')

def fps(mph):
	return mph*5280/3600

bb9.weight = 35
bb9.rho = 0.0023769
bb9.scale(1/12)
bb9.extra_drag = 0.0049*bb9.area
print(bb9.ar)

from chrysopelea import *

bb9 = dynamic('BB7.avl')
bb9.pop('VerTail')
bb9.pop('HTail')

def fps(mph):
	return mph*5280/3600

bb9.weight = 35
bb9.rho = 0.0023769
print(bb9.drag(fps(50)))

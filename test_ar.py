from chrysopelea import *

bb9 = dynamic('BB7.avl')
bb9.pop('VerTail')
bb9.pop('HTail')
bb9.set_attitude(cl=1)
print(bb9.cl,bb9.cdi,bb9.alpha)
bb9.set_attitude(cl = 0)
print(bb9.cl,bb9.cdi,bb9.alpha)
print(bb9.cd0)

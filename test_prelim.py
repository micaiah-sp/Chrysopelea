from preliminary import *

#carl.size()
p = preliminary()
p.takeoff = 100
p.v_max = 80
p.climb = (10,40)
p.turn = (2,50)
p.acceleration = (1,70)
p.size()
"""
w = 55
c = 5
v = 65
sintheta = c/v
war = 0.19666667
p.cd0 = 0.018
#p.inspect_ar(v,20,w-12*war,war,sintheta)
p.inspect_ar(v,20,8,war,sintheta)
"""

plt.show()

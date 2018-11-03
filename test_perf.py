from chrysopelea import *

bb7 = imperial_dynamic("BB7.avl")
"""
bb7.pop("HTail")
bb7.pop("VerTail")
"""
bb7.scale(1/12)

bb7.motor.static_thrust=11
bb7.motor.thrust_at_max=8
bb7.motor.max = 50*5280/3600
bb7.weight = 55
bb7.extra_drag = 0.018 - bb7.cd0
bb7.pitch_trim = 'Elevator'
bb7.print()
"""
bb7.plot_bending_moment('Wing')
bb7.set_attitude(alpha=3)
bb7.plot_bending_moment('Wing')
"""
plt.show()

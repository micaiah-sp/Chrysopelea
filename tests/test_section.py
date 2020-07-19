from Section import *

# Test section from airfoil coordinates
s = Section("../airfoils/SD7062.dat")

s.set_attitude(alpha=10)
s.execute()
assert round(s.lift_coef(), 2) == 1.70
assert round(s.drag_coef(), 3) == 0.000

s.set_attitude()
s.set_reynolds(4.5e5)
s.execute()
assert round(s.lift_coef(), 2) == 0.00
assert round(s.drag_coef(), 3) == 0.015

# Test section from NACA designation
n = Naca("0012")

n.set_reynolds(1e6)
n.set_attitude(alpha=10)
n.execute()
assert round(n.lift_coef(), 2) == 1.08
assert round(n.drag_coef(), 3) == 0.015

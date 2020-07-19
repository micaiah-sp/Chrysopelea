from Surface import *

surf = Surface("test")
surf.add_Section(Naca("0012"))
surf.add_Section(Naca("0012", (0, 1, 0)))

assert surf.area() == 2
assert surf.mean_chord() == 1
assert surf.mean_aerodynamic_chord() == 1
assert surf.aspect_ratio() == 2

surf = Surface("test")
surf.yduplicate = None
surf.add_Section(Naca("0012"))
surf.add_Section(Naca("0012", position=(0, 1, 0), chord=0.5))
assert surf.area() == 0.75
assert surf.mean_chord() == 0.75
l = 0.5
assert round(surf.mean_aerodynamic_chord(), 10) == round(2/3*1*(1 + l + l**2)/(1 + l), 10)
assert surf.aspect_ratio() == 4/3

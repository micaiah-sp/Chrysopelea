from Avl import *

# change the command to run AVL if the default does not work
Avl.avl_cmd = "~/programs/Avl/bin/avl" 


# test construction
print("Full aircraft configuration")
a0 = Avl()
a0.origin = (0.8, 0, 0)

wing = Surface("wing")
wing.add_Section(Naca("2412", chord=1.5))
wing.add_Section(Naca("2412", position=(1.5, 3, 0), chord=0.5, incidence=-2))
a0.add_Surface(wing)

tail = Surface("tail")
sec0 = Naca("0010", position=(3, 0, 0), chord=0.7)
sec0.add_Control(Control("elevator", xhinge=0.7))
sec0.add_Control(Control("rudder", xhinge=0.7, signdup=-1))
tail.add_Section(sec0)
sec1 = Naca("0010", position=(3, 1, -0.5), chord=0.5)
sec1.add_Control(Control("elevator", xhinge=0.8))
sec1.add_Control(Control("rudder", xhinge=0.8, signdup=-1))
tail.add_Section(sec1)
a0.add_Surface(tail)


# test drawing
print("Showing aircraft drawing.")
print("You should see an aircraft with a swept, tapered wing and an inverted V-tail.")
a0.draw()
print("Aircraft drawing closed.")
print()


# test aerodynamics
print("Inviscid aerodynamics:")
a0.set_attitude(alpha=10)
a0.execute()
a0.print_aerodynamics()
assert round(a0.induced_drag_coef(), 5) == round(a0.drag_coef(), 5)
print()

a0.set_attitude(alpha=10)
a0.reynolds = 5e5
print("Viscous aerodynamics with Re = {}".format(a0.reynolds))
a0.execute()
a0.print_aerodynamics()
print()

print("Uncambered untwisted wing")
a1 = Avl()

wing = Surface("wing")
wing.add_Section(Naca("0012", chord=1.5))
wing.add_Section(Naca("0012", position=(1.5, 3, 0), chord=0.5))
a1.add_Surface(wing)

a1.set_attitude(lift_coef=0)
a1.execute()
a1.print_aerodynamics()
assert round(a1.lift_coef(), 3) == 0
assert round(a1.induced_drag_coef(), 3) == 0
print()

print("Uncambered twisted wing")
a1.surfaces["wing"].sections[1].incidence = -10

a1.set_attitude(lift_coef=0)
a1.execute()
a1.print_aerodynamics()
assert round(a1.lift_coef(), 3) == 0
assert round(a1.angle_of_attack(), 3) > 0
assert round(a1.induced_drag_coef(), 3) > 0
print()

# Test stability and trim
print("Trimmed at lift coefficient 0.8 with 3 degree rudder deflection")
a0.set_attitude(lift_coef=0.8)
a0.set(a0.control_variables()["elevator"], "pm 0")
cons = "{} 3".format(a0.control_variables()["rudder"])
a0.set(a0.control_variables()["rudder"], cons)
a0.set("b", "ym 0")
a0.compute_stability=True
a0.execute()
a0.print_aerodynamics()
print("Sideslip: ", a0.sideslip())
print("Elevator deflection: ", a0.get_output("elevator"))
print("d Cm /d elevator: ", a0.get_control_derivative("Cm", "elevator"))
a0.print_stability()

# test writing/reading of AVL files
a0.name = "Test"
a0.write("test.avl")
a2 = Avl("test.avl")

from Avl import *

p = Avl()

m = Surface('Wing')
m.add_Section(Naca("0012", (0,0,0), 1))
n = Naca("0012", position=(0.5,1,0), chord=0.25+0.75/2)
n.add_Control(Control('elevon', xhinge=0.3, signdup=-1))
m.add_Section(n)
n = Naca("0012", position=(1,2,0), chord=0.25)
n.add_Control(Control('elevon', xhinge=0.3, signdup=-1))
m.add_Section(n)
m.add_Section(Naca("0012", (1.1, 2, 0.3), 0.2))
p.add_Surface(m)


print("MAC:", p.mean_aerodynamic_chord())
p.draw()
p.set("a", "a 5")
con = p.control_variables()['elevon']
p.set(con, '{} -5'.format(con))
p.execute(compute_stability=True, compute_moment_dist=True)
p.print_aerodynamics()
print("Lift to drag ratio:", p.lift_coef()/p.induced_drag_coef())
p.print_stability()
p.plot_bending_moment()
plt.show()

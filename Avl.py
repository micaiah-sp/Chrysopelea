from Surface import *
import matplotlib.pyplot as plt

class Avl:
    """
    class for performing AVL simulations

    Trim Parameter Reference:
  A lpha
  B eta
  R oll  rate
  P itch rate
  Y aw   rate
  D<n>  <control surface>

    Constraint reference:
       A    alpha       =   0.000
       B    beta        =   0.000
       R    pb/2V       =   0.000
       P    qc/2V       =   0.000
       Y    rb/2V       =   0.000
       C    CL          =   0.000
       S    CY          =   0.000
       RM   Cl roll mom =   0.000
       PM   Cm pitchmom =   0.000
       YM   Cn yaw  mom =   0.000
       D<n> <control>   =   0.000

    (use lowercase)

    """
    text = ""
    pitch_trim = None
    mach = 0
    reynolds = None
    sym = (0, 0, 0)
    origin = (0, 0, 0)
    reference_surface_name = None
    avl_cmd = "avl"
    name = "Chrysopelea"

    def __init__(self, geom_file=None):
        self.computed_stability = False
        self.computed_moment_dist = False
        self.computed_force_dist = False
        self.executed = False
        self.surfaces = {}
        if not (geom_file is None):
            file_obj = open(geom_file)
            text = file_obj.read()
            file_obj.close()

            text = re.sub('#.*','',text)
            surf_texts = re.split('SURFACE\n',text)
            header = surf_texts.pop(0)
            header = [e for e in re.split('\n|\t| ', header)[1:] if e != '']
            self.name = header.pop(0)
            header = [float(e) for e in header]
            self.mach = header[0]
            self.sym = (int(header[1]), int(header[2]), int(header[3]))
            self.origin = (header[7], header[8], header[9])
            for surf_text in surf_texts:
                self.add_Surface(Surface.from_text(surf_text))
        self.constraints = {}

    def reference_chord(self):
        return self.mean_chord()

    def __repr__(self):
        return "AVL interface object with surfaces {}".format(self.surfaces)

    def __str__(self):
        sym = "{} \t{} \t{}".format(self.sym[0], self.sym[1], self.sym[2])
        area = "{} \t{} \t{}".format(self.area(), self.reference_chord(), self.span())
        ref = "{} \t{} \t{}".format(self.origin[0], self.origin[1], self.origin[2])
        text = """
#Name of configuration
{}
#MACH
{}
#IYsym \tIZsym \tZsym \tVehicle \tSymmetry
{}
#Sref \tCref \tBref \tReference \tArea \tand \tLengths
{}
#Xref \tYref \tZref \tCenter \tof \tGravity \tLocation
{}
""".format(self.name, self.mach, sym, area, ref)
        for s in self.surfaces.keys():
            text += str(self.surfaces[s])
        return text

    def write(self, file_name):
        out_file = open(file_name, "w")
        out_file.write(str(self))
        out_file.close()

    def reference_surface(self):
        return self.surfaces[self.reference_surface_name]

    def area(self):
        return self.reference_surface().area()

    def mean_chord(self):
        return self.reference_surface().mean_chord()

    def mean_aerodynamic_chord(self):
        return self.reference_surface().mean_aerodynamic_chord()

    def span(self):
        return self.reference_surface().span()

    def aspect_ratio(self):
        return self.reference_surface().aspect_ratio()

    def add_Surface(self, surf):
        if type(surf) == str:
            surf = Surface(surf)
        if self.reference_surface_name is None:
            self.reference_surface_name = surf.name
        surf.parent = self
        self.surfaces[surf.name] = surf

    def operations_from_constraints(self):
        operations = ""
        cons = list(self.constraints)
        for c in cons:
            operations += "\n{}\n{}".format(c,self.constraints[c])
            self.constraints.pop(c)
        return operations

    def execute(self, operations="", compute_stability=False, compute_moment_dist=False, compute_force_dist=False, plot_treffitz=False):
        input_file = open('chrysopelea.avl','w')
        input_file.write(str(self))
        input_file.close()
        cmds = open('chrysopelea.ain','w')
        operations += self.operations_from_constraints()
        operations += '\nx'
        self.executed = True
        if compute_stability:
            operations += "\nST\n"
            self.computed_stability = True
        if compute_moment_dist:
            operations += '\nvm\nchrysopelea.amdist'
            self.computed_moment_dist = True
        if compute_force_dist:
            operations += '\nfs\nchrysopelea.afdist'
            self.computed_force_dist = True
        if plot_treffitz:
            operations += "\nt\nh"
        operations += '\n'
        cmd_text = """
load chrysopelea.avl
oper{}

quit

""".format(operations)
        cmds.write(cmd_text)
        cmds.close()
        subprocess.run(self.avl_cmd + " < chrysopelea.ain > chrysopelea.aout", shell=True)

        out = open("chrysopelea.aout")
        out_text = out.read()
        out.close()

        if compute_moment_dist:
            out = open("chrysopelea.amdist")
            self.moment_data = out.read()
            out.close()
        if compute_force_dist:
            out = open("chrysopelea.afdist")
            self.force_data = out.read()
            out.close()

        self.output = out_text

        if not (self.reynolds is None):
            for surf_name in self.surfaces.keys():
                surf = self.surfaces[surf_name]
                surf.set_reynolds()
                surf.set_attitude(self.angle_of_attack())
                surf.execute()
        return out_text

    def clear_constraints(self):
        self.constraints = {}

    def draw(self):
        operations = """
g
k"""
        self.execute(operations)

    def pop(self, surfname):
        if surfname in self.surfaces:
            return self.surfaces.pop(surfname)

    def control_variables(self):
        s = str(self)
        cs = s.split('CONTROL')[1:]
        controls = {}
        n = 1
        for c in cs:
            c = re.sub('#.*','',c)
            c = [cc for cc in re.split('\n|\t', c) if cc != ''][0].replace(" ", "")
            if c not in controls:
                controls[c] = 'd{}'.format(n)
                n += 1
        return controls

    def set(self, variable, constraint):
        self.constraints[variable] = constraint

    def set_attitude(self, lift_coef=None, alpha=0):
        """
        constrain alpha either directly or with cl.
        Included primarily for backwards compatability.
        """
        if not (lift_coef is None):
            self.set('a','c {}'.format(lift_coef))
        else:
            self.set('a','a {}'.format(alpha))
        if not (self.pitch_trim is None):
            d = self.control_variables()[self.pitch_trim]
            self.set(d,'pm 0')

    def get_control_derivative(self, variable, control):
        control_var = self.control_variables()[control]
        return self.get_output(variable + control_var)

    def get_output(self, variable):
        text = self.output.split('Vortex Lattice Output -- Total Forces')[-1]
        try:
            text = re.split("{} *= *".format(variable),text)[1].split(' ')[0]
        except:
            raise Exception("Failed to obtain output variable.")
        return float(text)

    def moment_dist(self, surf=None):
        if not self.computed_moment_dist:
            raise Exception("`execute` method of this object must be invoked with `compute_moment_dist = True`.")
        if surf is None:
            surf = self.reference_surface()
        text = self.moment_data.split(surf.name)[1]
        text = re.split('\n *\n', text)[0]
        text = '\n'.join(text.split('\n')[3:])
        text = re.sub(' +', ',', text)
        text = re.sub('\n,', '\n', text)
        text = re.sub('(^,)|(,$)', '', text)
        f = io.StringIO(text)
        return pd.read_csv(f)

    def force_dist(self, surf=None):
        if not self.computed_force_dist:
            raise Exception("`execute` method of this object must be invoked with `compute_force_dist = True`.")
        if surf is None:
            surf = self.reference_surface()
        text = self.force_data.split(surf.name)[1]
        text0 = self.force_data.split("Strip Forces referred to Strip Area, Chord")[1]
        text0 = re.split('\n *\n', text0)[0]
        text1 = self.force_data.split("Strip Forces referred to Strip Area, Chord")[2]
        text1 = re.split('\n *\n', text1)[0]
        text = text0 + '\n' + '\n'.join(text1.split('\n')[2:-2])
        text = re.sub(' +', ',', text)
        text = re.sub('(^,)|(,$)', '', text)
        f = io.StringIO(text)
        data = pd.read_csv(f)
        data.sort_values(axis=0, by='Yle', inplace=True)
        return data

    def plot_bending_moment(self, surf=None):
        if not self.computed_moment_dist:
            raise Exception("`execute` method of this object must be invoked with `compute_moment_dist = True`.")
        if surf is None:
            surf = self.reference_surface()
        dist = self.moment_dist(surf)
        plt.plot(dist.iloc[:,0], dist.iloc[:,1])
        plt.xlabel('Semispan Location')
        plt.ylabel('Moment per (unit span * unit area * unit dynamic pressure)')
        plt.title('Bending Moment for alpha = {}'.format(self.angle_of_attack()))

    def assert_stability(self):
        if not self.computed_stability:
            raise Exception("`execute` method of this object must be invoked with `compute_stability = True`.")

    def assert_executed(self):
        if not self.executed:
            raise Exception("`execute` method of this object must be invoked.")

    def Cl_beta(self):
        self.assert_stability()
        return self.get_output('Clb')

    def Cm_alpha(self):
        self.assert_stability()
        return self.get_output('Cma')

    def Cn_beta(self):
        self.assert_stability()
        return self.get_output('Cnb')

    def CL_alpha(self):
        self.assert_stability()
        return self.get_output('CLa')

    def aerodynamic_center(self):
        return -self.Cm_alpha()*self.reference_chord()/self.CL_alpha() + self.origin[0]

    def lift_coef(self):
        self.assert_executed()
        return self.get_output('CLff')

    def induced_drag_coef(self):
        self.assert_executed()
        return self.get_output('CDff')

    def drag_coef(self):
        drag = self.induced_drag_coef()*self.area()
        for surf_name in self.surfaces.keys():
            surf = self.surfaces[surf_name]
            drag += surf.drag_coef_2D()*surf.area()
        return drag/self.area()

    def print_aerodynamics(self):
        print("Angle of attack: ", self.angle_of_attack())
        print("Lift coefficient: ", self.lift_coef())
        print("Induced drag coefficient: ", self.induced_drag_coef())
        print("Drag coefficient: ", self.drag_coef())

    def print_stability(self):
        print("Aerodynamic center: ", self.aerodynamic_center())
        print("Cl_beta: ", self.Cl_beta())
        print("Cm_alpha: ", self.Cm_alpha())
        print("Cn_beta: ", self.Cn_beta())
        print("moment_x: ", self.moment_x())
        print("moment_y: ", self.moment_y())
        print("moment_z: ", self.moment_z())

    def moment_x(self):
        self.assert_executed()
        return self.get_output('Cltot')

    def moment_y(self):
        self.assert_executed()
        return self.get_output('Cmtot')

    def moment_z(self):
        self.assert_executed()
        return self.get_output('Cntot')

    def angle_of_attack(self):
        self.assert_executed()
        return self.get_output('Alpha')

    def sideslip(self):
        self.assert_executed()
        return self.get_output('Beta')

    def spanwise_efficiency(self):
        self.assert_executed()
        return self.get_output('e')

    def scale(self, factor):
        self.origin = (self.origin[0]*factor, self.origin[1]*factor, self.origin[2]*factor)
        for s in self.surfaces.keys():
            self.surfaces[s].scale(factor)

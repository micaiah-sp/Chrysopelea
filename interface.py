import math
import subprocess
from collections import OrderedDict
import re
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import time

########## AVL Class ##################

avl_path = "~/programs/Avl/bin/avl"

class avl:
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
    output = None
    moment_dist = None
    force_dist = None
    pitch_trim = None
    mach = 0
    xyzsym = (0,0,0)
    xyzref = (0,0,0)
    

    def __init__(self,file=None):
        self.compute_stability = False
        self.compute_moment_dist = False
        self.compute_force_dist = False
        self.surfaces = {}
        if file != None:
            file_obj = open(file)
            text = file_obj.read()
            file_obj.close()

            text = re.sub('#.*','',text)
            stexts = re.split('SURFACE\n',text)
            header = stexts.pop(0)
            header = [float(e) for e in re.split('\n|\t| ',header)[1:] if e != '']
            self.mach = header[0]
            self.xyzsym = (int(header[1]),int(header[2]),int(header[3]))
            self.xyzref = (header[7],header[8],header[9])
            for stext in stexts:
                self.add_surface(Surface.from_text(stext))
        self.constraints = {}

    @property
    def cref(self):
        return self.mean_chord

    def __repr__(self):
        return "AVL interface object with surfaces {}".format(self.surfaces)

    def __str__(self):
        sym = "{}         {}         {}".format(self.xyzsym[0],self.xyzsym[1],self.xyzsym[2])
        area = "{}         {}         {}".format(self.area,self.cref,self.span)
        ref = "{}         {}         {}".format(self.xyzref[0],self.xyzref[1],self.xyzref[2])
        text = """
Advanced
#MACH
{}
#IYsym        IZsym        Zsym        Vehicle Symmetry
{}
#Sref        Cref        Bref        Reference Area and Lengths
{}
#Xref         Yref         Zref         Center of Gravity Location
{}
""".format(self.mach,sym,area,ref)
        for s in list(self.surfaces):
            text += str(self.surfaces[s])
        return text

    @property
    def area(self,ref_surf_name='Wing'):
        if ref_surf_name in self.surfaces.keys():
            return self.surfaces[ref_surf_name].area
        else:
            return 1

    @property
    def mean_chord(self,ref_surf_name='Wing'):
        if ref_surf_name in self.surfaces.keys():
            return self.surfaces[ref_surf_name].mean_chord
        else:
            return 1

    @property
    def mean_aerodynamic_chord(self,ref_surf_name='Wing'):
        if ref_surf_name in self.surfaces.keys():
            return self.surfaces[ref_surf_name].mean_aerodynamic_chord
        else:
            return 1

    @property
    def span(self,ref_surf_name='Wing'):
        if ref_surf_name in self.surfaces.keys():
            return self.surfaces[ref_surf_name].span
        else:
            return 1

    @property
    def ar(self,ref_surf_name='Wing'):
        if ref_surf_name in self.surfaces.keys():
            return self.surfaces[ref_surf_name].ar
        else:
            return 1

    def add_surface(self,surf):
        if type(surf) == str:
            surf = Surface(surf)
        surf.parent = self
        self.surfaces[surf.name] = surf

    def operations_from_constraints(self):
        operations = ""
        cons = list(self.constraints)
        for c in cons:
            operations += "\n{}\n{}".format(c,self.constraints[c])
            self.constraints.pop(c)
        return operations

    def execute(self,operations=None):
        input = open('chrysopelea.avl','w')
        input.write(str(self))
        input.close()
        cmd = open('chrysopelea.ain','w')
        opArg = operations
        if operations is None:
            operations = self.operations_from_constraints()
            operations += '\nx'
            if self.compute_stability:
                operations += "\nST"
            if self.compute_moment_dist:
                operations += '\nvm\nchrysopelea.m_dis'
            if self.compute_force_dist:
                operations += '\nfs\nchrysopelea.f_dis'
        operations += '\n'
        cmd_text = """
load chrysopelea.avl
oper{}
quit

""".format(operations)
        #print(cmd_text)
        cmd.write(cmd_text)
        cmd.close()
        with open("chrysopelea_subproc_out","w") as subproc_out:
            subprocess.run(avl_path + "<chrysopelea.ain>chrysopelea.aot",\
                shell=True,stderr=subproc_out)

        out = open("chrysopelea.aot")
        out_text = out.read()
        out.close()

        if opArg is None:
            if self.compute_moment_dist:
                out = open("chrysopelea.m_dis")
                self.moment_dist = out.read()
                out.close()
            if self.compute_force_dist:
                out = open("chrysopelea.f_dis")
                self.force_dist = out.read()
                out.close()


        self.output = out_text
        return out_text

    def clear_constraints(self):
        self.constraints = {}

    def draw(self):
        operations = """
g
k"""
        self.execute(operations)
        self.output = None

    def pop(self, surname):
        if surname in self.surfaces:
            return self.surfaces.pop(surname)

    def control_variables(self):
        s = str(self)
        cs = s.split('CONTROL')[1:]
        controls = {}
        n = 1
        for c in cs:
            c = re.sub('#.*','',c)
            c = [cc for cc in re.split('\n|\t| ',c) if cc != ''][0]
            if c not in controls:
                controls[c] = 'd{}'.format(n)
                n += 1
        return controls

    def set(self,var,cons):
        self.constraints[var] = cons
        self.output=None
        self.moment_dist = None
        self.force_dist = None

    def set_attitude(self,cl=None,alpha=0):
        """
        constrain alpha either directly or with cl.
        Included primarily for backwards compatability.
        """
        if cl != None:
            self.set('a','c {}'.format(cl))
        elif alpha != None:
            self.set('a','a {}'.format(alpha))
        if self.pitch_trim != None:
            d = self.control_variables()[self.pitch_trim]
            self.set(d,'pm 0')

    def stability(self):
        stab = self.compute_stability
        self.compute_stability = True
        self.execute()
        self.compute_stability = stab

    def get_control_derivative(self, var, control):
        con = self.control_variables()[control]
        return self.get_stab(var + con)

    def get_output(self,var):
        if not self.output:
            self.execute()
        text = self.output.split('Vortex Lattice Output -- Total Forces')[-1]
        text = re.split("{} *= *".format(var),text)[1].split(' ')[0]
        return float(text)

    def get_stab(self,var):
        try:
            return self.get_output(var)
        except:
            self.stability()
            return self.get_output(var)

    def get_moment_dist(self,surf):
        if not self.moment_dist:
            compute_md = self.compute_moment_dist
            self.compute_moment_dist = True
            print("re-executing")
            self.execute()
            self.compute_moment_dist = compute_md
        text = self.moment_dist.split(surf)[1]
        text = re.split('\n *\n',text)[0]
        text = '\n'.join(text.split('\n')[3:])
        text = re.sub(' +',',',text)
        text = re.sub('\n,','\n',text)
        text = re.sub('(^,)|(,$)','',text)
        f = io.StringIO(text)
        return pd.read_csv(f)

    def get_force_dist(self,surf):
        if not self.force_dist:
            compute_fd = self.compute_force_dist
            self.compute_force_dist = True
            print("re-executing")
            self.execute()
            self.compute_force_dist = compute_fd
        text = self.force_dist.split(surf)[1]
        text0 = self.force_dist.split("Strip Forces referred to Strip Area, Chord")[1]
        text0 = re.split('\n *\n',text0)[0]
        text1 = self.force_dist.split("Strip Forces referred to Strip Area, Chord")[2]
        text1 = re.split('\n *\n',text1)[0]
        text = text0 + '\n' + '\n'.join(text1.split('\n')[2:-2])
        text = re.sub(' +', ',', text)
        text = re.sub('(^,)|(,$)','', text)
        f = io.StringIO(text)
        data = pd.read_csv(f)
        data.sort_values(axis=0,by='Yle',inplace=True)
        return data

    def compute_Cl(self, surf):
        force_data = self.get_force_dist(surf)
        moment = force_data.loc[:, 'cl'] * force_data.loc[:, 'Area'] * force_data.loc[:, 'Yle']
        moment = moment.sum()
        return moment / (self.area * self.span)

    def compute_Cn(self, surf):
        force_data = self.get_force_dist(surf)
        #force_data[ 'd' ] = force_data.loc[:, 'cl'] * force_data.loc[:, 'ai'] * np.pi/180 * force_data.loc[:, 'Area' ]
        force_data[ 'd' ] = force_data.loc[:, 'ai'] * np.pi/180 * force_data.loc[:, 'Area' ]
        print(force_data)
        moment = force_data.loc[:, 'cl'] * force_data.loc[:, 'ai'] * -np.pi/180 *\
                 force_data.loc[:, 'Area'] * force_data.loc[:, 'Yle']
        moment = moment.sum()
        return moment / (self.area * self.span)

    def plot_bending_moment(self,surf):
        dist = self.get_moment_dist(surf)
        plt.plot(dist.iloc[:,0],dist.iloc[:,1])
        plt.xlabel('Semispan Location')
        plt.ylabel('Moment per (unit span * unit area * unit dynamic pressure)')
        plt.title('Bending Moment for alpha = {}'.format(self.alpha))

    @property
    def Cl_beta(self):
        return self.get_stab('Clb')

    @property
    def Cm_alpha(self):
        return self.get_stab('Cma')

    @property
    def Cn_beta(self):
        return self.get_stab('Cnb')

    @property
    def CL_alpha(self):
        return self.get_stab('CLa')

    @property
    def xac(self):
        return -self.Cm_alpha*self.cref/self.CL_alpha

    @property
    def CL(self):
        return self.get_output('CLff')
    @property
    def CDi(self):
        return self.get_output('CDff')

    @property
    def Cl(self):
        return self.get_output('Cltot')

    @property
    def Cm(self):
        return self.get_output('Cmtot')

    @property
    def Cn(self):
        return self.get_output('Cntot')

    @property
    def alpha(self):
        return self.get_output('Alpha')

    @property
    def e(self):
        return self.get_output('e')

    def scale(self, factor):
        self.xyzref = (self.xyzref[0]*factor,self.xyzref[1]*factor,self.xyzref[2]*factor)
        for s in self.surfaces.keys():
            self.surfaces[s].scale(factor)

    def set_nchord(self,nc):
        for k in self.surfaces.keys():
            self.surfaces[k].nchord = nc
    def set_nspan(self,ns):
        for k in self.surfaces.keys():
            self.surfaces[k].set_nspan(ns)

class fast_avl(avl):
    memory_df = pd.DataFrame({'Alpha':[],'CLtot':[],'CDind':[],'e':[]})
    mesh_size = 0.5
    output_df = None

    def set_attitude(self,cl=None,alpha=0):
        if self.memory_df.empty:
            avl.set_attitude(self,cl=cl,alpha=alpha)
            self.to_df()
        if cl != None:
            paramname = 'CLtot'
            paramvalue = cl
        elif alpha != None:
            paramname = 'Alpha'
            paramvalue = alpha
        while True:
            self.memory_df.sort_values(paramname,inplace=True)
            greater = self.memory_df.loc[self.memory_df[paramname] >= paramvalue]
            less = self.memory_df.loc[self.memory_df[paramname] < paramvalue]
            if (len(greater) > 0) and (len(less) > 0):
                greater, less = greater.iloc[0], less.iloc[-1]
                output_ser = less + (greater-less)*(paramvalue-less[paramname])/(greater[paramname]-less[paramname])
                self.output_df = pd.DataFrame(output_ser).transpose()
                return self.output_df
            elif len(greater) == 0:
                alpha = less.iloc[-1]['Alpha'] + self.mesh_size
            else:
                alpha = greater.iloc[0]['Alpha'] - self.mesh_size
            avl.set_attitude(self,alpha=alpha)
            self.to_df()

    def plot_mem(self):
        plt.plot(self.memory_df['CDind'],self.memory_df['CLtot'])
        plt.show()

    def reset(self):
        self.memory_df = pd.DataFrame({'Alpha':[],'CLtot':[],'CDind':[],'e':[]})

    def to_df(self):
        new_df = pd.DataFrame({'Alpha':[avl.get_output(self,'Alpha')],'CLtot':[avl.get_output(self,'CLtot')],\
'CDind':[avl.get_output(self,'CDind')],'e':[avl.get_output(self,'e')]})
        self.memory_df = pd.concat([self.memory_df, new_df])

    def get_output(self,var):
        if self.output_df is None:
            self.set_attitude
        return self.output_df[var][0]


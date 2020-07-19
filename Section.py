import subprocess
import io
import re
import pandas as pd

class Section:
    polar = None
    parent = None
    reynolds = None
    xfoil_cmd = "xfoil"

    def __init__(self, coord_file, position=(0,0,0), chord=1,\
                 incidence=0, sspace=1, nspan=10):
        self.controls = []
        self.coord_file = coord_file
        self.position = position
        self.chord = chord
        self.incidence = incidence

    @classmethod
    def from_text(cls, text):
        entries = re.split('\n|\t',text)
        entries = [e for e in entries if e != '']
        coord = (float(entries[0]), float(entries[1]), float(entries[2]))
        chord = float(entries[3])
        sspace = int(entries[5]); nspan = int(entries[6])
        idientity = cls.identity_from_text(text)
        section = cls(identity, position=coord, chord=chord, sspace=sspace, nspan=nspan)
        section.add_control_from_text(text)
        return section

    @classmethod
    def identity_from_text(cls, text):
        afile = re.split('AFILE\n*\t*',text)
        afile = afile[1]
        afile = re.split('\n|\t',afile)[0]
        return afile

    def add_control(self, control):
        control.parent = self
        self.controls.append(control)

    def add_control_from_text(self,text):
        con = text.split('CONTROL')
        if len(con) > 1:
            con = Control.from_text(con[1])
            self.add_control(con)

    def drag_coef(self):
        return self.polar.iloc[0]['CD']

    def lift_coef(self):
        return self.polar.iloc[0]['CL']

    def set_attitude(self, alpha=None, CL=0):
        if not (alpha is None):
            self.attitude = "alfa {}".format(alpha + self.incidence)
        else:
            self.attitude = "CL {}".format(CL)

    def set_reynolds(self, value=None):
        if value:
            self.reynolds = value
        else:
            return self.parent.parent.reynolds()*self.chord / \
                   self.parent.parent.ref_chord()
        self.reynolds = int(self.reynolds)

    def load_cmd(self):
        return "load {}".format(self.coord_file)

    def load_text(self):
        return "AFILE\n{}".format(self.coord_file)

    def misc_cmds(self):
        return ""

    def execute(self):
        input = open("chrysopelea.xin",'w')
        if self.reynolds:
            reynolds_cmd = "\nvisc {}".format(self.reynolds)
        else:
            reynolds_cmd = ""
        xfoil_cmds = """
{}
{}
oper{}
pacc
chrysopelea.xpolar

{}

quit
""".format(self.load_cmd(), self.misc_cmds(), reynolds_cmd, self.attitude)
        input.write(xfoil_cmds)
        input.close()
        cmd = "{} < chrysopelea.xin > chrysopelea.xout".format(self.xfoil_cmd)
        subprocess.run(cmd, shell=True)

        polar = open("chrysopelea.xpolar")
        text = polar.read()
        polar.close()
        csv = io.StringIO(re.sub(' +', ',', text))
        polar = pd.read_csv(csv,skiprows = list(range(10)) + [11])
        polar.dropna(axis=1,inplace=True)
        self.polar = polar
        # prevents appending to the same file
        subprocess.run("rm chrysopelea.xpolar", shell=True)

    def __str__(self):
        # Trailing space at end of {} line is necessary!
        s = """
#----------------------------------------------
SECTION
#Xle         Yle         Zle         Chord         Ainc         Nspan         Sspace
{}          {}          {}          {}          {}          {}          {} 
{}""".format(self.position[0], self.position[1], self.position[2], self.chord, \
             self.incidence, self.nspan, self.sspace, self.load_text())
        for con in self.controls:
            s += str(con)
        return s

    def translate(self, coord):
        self.position = tuple([self.position[i] + coord[i] for i in range(3)])

class Naca(Section):
    def __init__(self, desig, position=(0,0,0), chord=1, incidence=0, sspace=1, nspan=10):
        self.controls = []
        self.desig = desig
        self.position = position
        self.chord = chord
        self.sspace = sspace
        self.nspan = nspan

    @classmethod
    def identity_from_text(cls, text):
        desig = re.split('NACA\n*\t*',text)
        desig = re.split('\n|\t| ',desig[1])[0]
        return desig

    def load_cmd(self):
        return "naca {}".format(self.desig)

    def load_text(self):
        return "NACA\n{}".format(self.desig)

def section_from_text(text):
    if "NACA" in text:
        return Naca.from_text(text)
    else:
        return Section.from_text(text)

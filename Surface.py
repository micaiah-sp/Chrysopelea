from Section import *
import math

class Surface:
    yduplicate = 0
    parent = None

    def __init__(self, name, cspace=1, nchord=5):
        self.sections = []
        self.name = name
        self.cspace = 1
        nchord = 5

    def add_Section(self, sec):
        sec.parent=self
        self.sections.append(sec)

    def __repr__(self):
        return 'AVL surface with name "{}"'.format(self.name)

    def __str__(self):
        # important note: spaces after numbers in Nchord... !!
        if self.yduplicate == None:
            ydup = ""
        else:
            ydup = "YDUPLICATE\n" + str(self.yduplicate)
        text = """
#==============================================
SURFACE
{}""".format(self.name)
        text += """
#Nchord        Cspace 
{}         {} 
{}""".format(self.nchord,self.cspace,ydup)

        for s in self.sections:
            text += str(s)
        return text

    def area(self):
        """
        return the planform area
        """
        a = 0
        for n in range(1,len(self.sections)):
            a += 0.5*abs(self.sections[n].position[1] - self.sections[n-1].position[1]) \
                    *(self.sections[n].chord + self.sections[n-1].chord)
        if self.yduplicate is None:
            return a
        else:
            return a*2

    def span(self):
        a = 0
        pos = [s.position[1] for s in self.sections]
        if self.yduplicate is None:
            b = abs(max(pos) - min(pos))
        else:
            b = 2*max([abs(p-self.yduplicate) for p in pos])
        return b

    def mean_chord(self):
        return self.area()/self.span()

    def mean_aerodynamic_chord(self):
        def integrated_sq_chord(sect0, sect1):
            if (sect0.chord == sect1.chord):
                return sect0.chord**2 * self.dist(sect0, sect1)
            return (sect0.chord**3 - sect1.chord**3)/3 \
                   * self.dist(sect0, sect1)/(sect0.chord - sect1.chord)
        total = 0
        for iSect in range(1, len(self.sections)):
            total += integrated_sq_chord(self.sections[iSect], self.sections[iSect - 1])
        if self.yduplicate is None:
            return total/self.area()
        else:
            return total*2/self.area()

    def aspect_ratio(self):
        return self.span()/self.mean_chord()

    @staticmethod
    def dist(sec0, sec1):
        d1 = sec0.position[1] - sec1.position[1]
        d2 = sec0.position[2] - sec1.position[2]
        return math.sqrt(d1**2 + d2**2)

    def drag_coef_2D(self):
        c = 0
        for n in range(1,len(self.sections)):
            c0 = self.sections[n].drag_coef()*self.section[n].chord
            c1 = self.sections[n-1].drag_coef()*self.sections[n].chord
            chordwise = 0.5*(c0 + c1)
            c += chordwise*self.dist(self.sections[n], self.sections[n - 1])
        if not (self.yduplicate is None):
            c *= 2
        return c/self.area()

    @classmethod
    def from_text(cls, text):
        text = re.sub('\n+','\n',text)
        sects = text.split('SECTION')
        head = sects.pop(0)
        name = head.split('\n')[0]
        s = Surface(name)
        parts = head.split('TRANSLATE')
        if len(parts) > 1:
            entries = re.split('\n|\t',parts[1])
            entries = [e for e in entries if e != '']
            delta = (float(entries[0]), float(entries[1]), float(entries[2]))
        else:
            delta = (0,0,0)
        for sect in sects:
            section = section_from_text(sect)
            section.translate(delta)
            s.add_section(section)
        return s

    def scale(self, factor):
        for s in self.sections:
            s.position = [x*factor for x in s.position]
            s.chord *= factor

    def set_attitude(self, alpha):
        for sec in self.sections:
            sec.set_attitude(alpha=alpha)

    def execute(self):
        for sec in self.sections:
            sec.execute()

    def set_reynolds(self):
        for sec in self.sections:
            sec.set_reynolds()

class Control:

    def __init__(self, name, gain=1, xhinge=0.5, xyzhvec=(0,0,0), signdup=1):
        self.name = name
        self.gain = gain
        self.xhinge = xhinge
        self.xyzhvec = xyzhvec
        self.signdup = signdup

    @classmethod
    def from_text(cls, text):
        text = re.sub('#.*','',text)
        entries = [e for e in re.split('\n|\t| ',text) if e != '']
        return Control(entries[0], gain=entries[1], xhinge=entries[2],\
               xyzhvec=(entries[3], entries[4], entries[5]), signdup=entries[6])

    def __str__(self):
        # The space at the end of the last line is necessary
        string = """
CONTROL
#NAME         GAIN        XHINGE        XHVEC        YHVEC        ZHVEC        SIGNDUP
{}         {}         {}         {}         {}         {}         {} """
        return string.format(self.name, self.gain, self.xhinge, self.xyzhvec[0],\
                             self.xyzhvec[1], self.xyzhvec[2], self.signdup)


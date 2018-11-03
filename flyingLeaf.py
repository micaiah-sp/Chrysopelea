from chrysopelea import *

span = 60
chord = 30
c = 30*0.7
sheet = Surface('Wing')
sheet.add_naca(position = (0,0,0),chord = c)
sheet.add_naca(position = (0,span/2),chord = c)

fl = avl()
fl.add_surface(sheet)
fl.draw()

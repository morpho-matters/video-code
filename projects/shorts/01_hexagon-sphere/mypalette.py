import morpholib as morpho
mo = morpho
import morpholib.color

import numpy as np

black = (0,0,0)
white = (1,1,1)
red = (1,0,0)
green = (0,1,0)
blue = (0,0,1)
myred = (0.8,0,0)
mygreen = (0,0.6,0)
darkgreen = dgreen = (0,0.5,0)
myblue = (0,0,0.8)
yellow = (1,1,0)
cyan = (0,1,1)
magenta = (1,0,1)
pink = tuple(mo.color.parseHexColor("ffc0cb"))
orange = tuple(mo.color.parseHexColor("ff6300"))
redorange = tuple(mo.color.parseHexColor("ff6600"))
redderorange = tuple(mo.color.parseHexColor("ff4400"))
yelloworange = tuple(mo.color.parseHexColor("ffbf00"))
violet = (mo.color.colormap["violet"])
lighttan = tuple(mo.color.parseHexColor("f4f1c1"))
goodblue = tuple((mo.array([0,0.5,1])*0.75).tolist())
softblue = tuple(mo.color.parseHexColor("248bad"))
lightblue = tuple(mo.color.parseHexColor("c1c1f4"))
babyblue = tuple(mo.color.parseHexColor("c1f4ef"))
vividblue = (0.25, 0.25, 0.8)
indigo = tuple(mo.color.parseHexColor("330099"))
lightbluegreen = tuple(mo.color.parseHexColor("c1f4ec"))
metallicblue = tuple(mo.color.parseHexColor("547071"))
lavender = tuple(mo.color.parseHexColor("dbc1f4"))
lightviolet = tuple((1-0.75*(1-np.array(violet))).tolist())
lightred = tuple(mo.color.parseHexColor("f4c1da"))
lightgreen = tuple(mo.color.parseHexColor("c1f4c2"))
grassgreen = tuple(mo.color.parseHexColor("05a700"))
brown = mo.color.colormap["brown"]
gray = grey = (0.5, 0.5, 0.5)
darkgray = darkgrey = dgray = dgrey = (1/3,)*3
gentleblue = tuple(mo.color.parseHexColor("88afe1"))
sandytan = tuple(mo.color.parseHexColor("e4d599"))
softpink = tuple(mo.color.parseHexColor("e19fb4"))

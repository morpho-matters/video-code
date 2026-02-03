
import morpholib as morpho
morpho.importAll()
mo = morpho  # Allows the shorthand "mo" to be used instead of "morpho"

# Import particular transition functions into the main namespace
from morpholib.transitions import uniform, quadease, drop, toss, \
    sineease, glide, coast
# Import useful functions and constants into the main namespace
from morpholib.tools.basics import *

# Import various other libraries
import math, cmath, random
import numpy as np

from mypalette import *
from myheader import *

# Set default transition to quadease
morpho.transition.default = quadease
# Set default font to be the LaTeX font
morpho.text.defaultFont = "CMU serif"


def main():
    # Define layers here
    mainlayer = morpho.Layer(view=mo.video.view169())
    mation = morpho.Animation([mainlayer])
    mation.windowShape = (round(9/16*1080), 1080)
    mation.fullscreen = True
    mation.background = lighttan







    print("Animation length:", mation.seconds())
    mation.wait(10*30)

    mation.finitizeDelays(30)

    # mation.start = mation.lastID()
    mation.locatorLayer = mainlayer
    mation.clickRound = 2
    mation.clickCopy = True
    # mation.newFrameRate(10)
    mation.play()

    # # Check that no bookmarks are active
    # assert (mation.firstID() if mation.start is None else mation.start) <= min([oo]+list(mation.delays.keys()))
    # mation.newFrameRate(8)
    # mation.export("./animation.mp4", scale=1)


main()

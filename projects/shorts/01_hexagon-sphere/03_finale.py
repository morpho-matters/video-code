
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
    layer3 = mo.SpaceLayer(view=mo.video.view169())
    mainlayer.camera.first().rescaleWidth(9/16)
    layer3.camera.first().rescaleWidth(9/16)
    layer2 = mainlayer.copy()
    mation = morpho.Animation([layer3, mainlayer, layer2])
    mation.windowShape = (int(9/16*1080), 1080)
    mation.fullscreen = True
    mation.background = lightblue

    SCALE = mation.windowShape[1] / 1080
    EDGEWIDTH = 5*SCALE

    # layer2.mask = mainlayer.copy()

    # layer3.camera.first().zoomIn(1)

    def poly(n, sidelength=1):
        polygon = mo.grid.MultiPath3D([1j*cmath.exp(tau/n*k*1j) for k in range(n)]).close().set(
            orientable=True,
            alphaFill=1
            )
        currentSidelength = abs(cmath.exp(tau/n*1j)-1)
        return polygon.fimage(lambda v: v*sidelength/currentSidelength)

    # Multiply edgelength by this to get the distance between the center of
    # a pentagonal face and the center of the soccer ball.
    heightScalar = 4.654876873532656/2

    sidelength = 2
    pent0 = poly(5, sidelength).set(
        width=EDGEWIDTH, color=black, fill=[0.15]*3
        )
    pents = [pent0]
    pentRadius = abs(pent0.seq[0])
    pentApothem = abs(mean(pent0.seq[:2]))
    hexApothem = poly(6, sidelength).boxWidth()/2

    # Do pi minus these angles to get relative rotation angles
    angle65 = math.acos(-math.sqrt((5+2*math.sqrt(5))/15))
    angle66 = math.acos(-math.sqrt(5)/3)
    angle55 = 2.0344439357957027

    rot65 = pi - angle65
    rot66 = pi - angle66
    rot55 = pi - angle55

    hexes = []
    for n in range(5):
        hx = poly(6, sidelength).fimage(lambda z: cmath.exp(tau/12*1j)*z).set(
            width=pent0.width, color=black, fill=white, # align=[0,-1],
            orient=(rot := mo.matrix.rotation(khat, tau/10+n*tau/5))@mo.matrix.rotation(ihat, angle65-pi),
            pos=mo.matrix.rotation(khat, tau/10+n*tau/5)@(pentApothem*jhat + hexApothem*mo.matrix.rotation(ihat, angle65-pi)@jhat)
            )
        hexes.append(hx)

    for n, hx in enumerate(hexes):
        center = hx.orient@mo.array(hx.center()) + hx.pos
        normal = hx.orient @ khat
        rot = mo.matrix.rotation(normal, tau/3)
        pent = pent0.copy().set(
            pos=center-rot@center,
            orient=rot
            )
        pents.append(pent)

    for shape in pents+hexes:
        shape.pos += sidelength*heightScalar*khat

    # Side hexagons
    sidehexes = []
    for hex1, hex2, pent in zip(hexes[:], hexes[1:]+hexes[:1], pents[1:]+pents[:1]):
        hex1 = hex1.copy()
        hex2 = hex2.copy()
        normal = pent.orient @ khat
        for hx in [hex1, hex2]:
            hx.set(
                pos=mo.matrix.rotation(normal, 2*tau/5)@(hx.pos-pent.pos)+pent.pos,
                orient=mo.matrix.rotation(normal, 2*tau/5) @ hx.orient
                )
            sidehexes.append(hx)


    top = mo.SpaceFrame(pents+hexes)
    mid = mo.SpaceFrame(sidehexes)
    # bottom = mo.SpaceFrame()
    bottom = top.copy()
    for shape in bottom.figures:
        shape.pos *= -1
        if len(shape.seq)-1 == 5:
            shape.rotation += tau/10
        # shape.orient *= -1

    soccer = layer3.Actor(top.merge([mid, bottom]))
    # Sort subfigures so pentagons are first then hexagons
    soccer.first().figures.sort(key=lambda fig: len(fig.seq))

    layer3.camera.newendkey(90)  # TBD
    layer3.camera.first().orient = mo.matrix.rotation(ihat, -179.99*deg) @ mo.matrix.rotation(khat, tau/5)
    layer3.camera.first().set(transition=uniform)

    soccer.fadeIn(15)
    layer3.camera.newkey(layer3.camera.firstID()+15)
    layer3.camera.first().moveBy(3j)

    soccerOrig = soccer.last().dup()

    # print("Decompose:", mation.seconds())

    side = sidelength*0.6
    pentarray = mo.combo.figureGrid(
        poly(5, side).set(
            width=pent0.width, color=black, fill=pent0.fill
            ),
        shape=(3,4),
        pos=8.75j, align=[0,1],
        width=8, height=4.75
        ).toType(mo.SpaceFrame)
    hexarray = mo.combo.figureGrid(
        poly(6, side).set(
            width=pent0.width, color=black, fill=white,
            rotation=tau/12
            ),
        shape=(5,4),
        pos=-8.5j, align=[0,-1],
        width=8, height=10
        ).toType(mo.SpaceFrame)

    polyarray = pentarray
    polyarray.merge(hexarray)

    soccer.newendkey()
    soccer.last().select[0].tweenMethod = mo.grid.MultiPath3D.tweenSpiral
    soccer.subtween(polyarray, 20, substagger=1, select=sel[:])





    ### ABOVE IS PRELIM ###

    mation.start = mation.lastID()


    layer3.camera.last().moveBy(-3.5j)

    # soccer.newendkey(instant=True).iall.pos += 4*jhat
    soccer.last().select[:-20].visible = False
    soccer.subaction.fadeIn(15, jump=2j, substagger=0.8, select=sel[-20:])


    mation.waitUntilSec(1.95)
    print("Reconstruct incomplete ball:", mation.seconds())

    # soccer.newendkey()
    # layer3.camera.newendkey()

    # soccer.subaction.fadeIn(15, jump=3j, substagger=1.5, select=sel[11::-1])
    # layer3.camera.newendkey(20).moveBy(3.5j)

    soccer.newendkey()
    layer3.camera.newendkey().transition = uniform

    soccer.newendkey(20, soccerOrig).select[:12].visible = False

    soccer.newkey(mation.timelineCoord(3.5), instant=True).select[:12].set(
        visible=True,
        transform=mo.matrix.scale2d(0)
        )
    print("Show pentagons:", mation.seconds())

    soccer.newendkey(15).select[:12].transform = I2

    layer3.camera.newendkey(1.5*30, layer3.camera.first().dup(), glob=True).moveBy(-3j)
    # layer3.camera.last().orient = np.linalg.matrix_power(layer3.camera.key[-1].orient, 2)
    layer3.camera.newkey(soccer.keyID(-3)).centerAt(layer3.camera.last().center())




    print("Animation length:", mation.seconds())
    # mation.wait(3*30)

    # mation.finitizeDelays(30)

    # mation.start = mation.lastID()
    mation.locatorLayer = mainlayer
    mation.clickRound = 2
    mation.clickCopy = True
    # mation.newFrameRate(10)
    # mation.play()

    # print(mation.windowShape)

    # # Check that no bookmarks are active
    # # assert (mation.firstID() if mation.start is None else mation.start) <= min([oo]+list(mation.delays.keys()))
    mation.rescale(1920/1080)
    mation.newFrameRate(60)
    mation.export("./03_finale.mp4", scale=1)


main()

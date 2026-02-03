
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
    toplayer = mainlayer.copy()
    mation = morpho.Animation([layer3, mainlayer, layer2, toplayer])
    mation.windowShape = (int(9/16*1080), 1080)
    # mation.windowShape = (1080, 1920)
    mation.fullscreen = True
    mation.background = lightblue

    layer2.mask = mainlayer.copy()

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
        width=5, color=black, fill=[0.15]*3
        )

    mation.waitUntilSec(7.65)
    print("Show hex ball:", mation.seconds())

    rim = mainlayer.Actor(mo.grid.ellipse(0,5).set(
        width=6, color=black,
        fill=mo.color.RadialGradientFill(0,
            r0=1, r1=6.5, gradient=mo.color.Gradient({
                0: [1]*3,
                1: [0.55]*3
                }),
            origin=-1-1j
            )
        ).toPath())


    radius = 1
    hexbase = mo.grid.Path([radius*cmath.exp(n*tau/6*1j) for n in range(6)]).close().set(
        width=pent0.width, color=black, fill=white, alphaFill=0
        ).insertNodesUniformly(30)
    hapo = hexbase.boxHeight()/2

    trimat = 2*hapo*mo.matrix.mat(math.sqrt(3)/2, 1/2, 0, 1).T
    basepts = np.array(range(-3,4))[:,None] + np.array(range(-3,4))[None,:]*1j
    basepts = basepts.reshape(-1).tolist()
    hexcenters = [trimat*z for z in basepts]

    hexgrid = layer2.Actor(mo.Frame([hexbase.copy().set(origin=z) for z in hexcenters]))
    hexgrid.last().all.commitTransforms()
    hexgrid.last().select[::4].set(
        fill=black, alphaFill=0.85
        )

    ballmask = layer2.mask.Actor(rim.last().dup().set(
        width=0, fill=black,
        modifier=lambda self: self._updateFrom(rim.now(), common=True, ignore={"fill", "width"})
        ))

    rim.popIn(15)
    # hexgrid.subaction.popIn(15)

    mation.wait(5)

    imposs = mainlayer.Actor(mo.text.Text("Impossible!",
        pos=rim.last().top()+1j, align=[0,-1],
        size=84, color=myred
        ))
    imposs.fadeIn(12, jump=2j)

    mation.waitUntilSec(11.2)
    print("Contort hex grid:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    hexgrid.newendkey().all.set(tweenMethod=mo.grid.Path.tweenSpiral)
    def contortion(z): return z*cmath.exp(abs(z)*1j/3)
    hexgrid.newendkey(30, hexgrid.last().fimage(contortion))

    mation.waitUntilSec(13.5)
    print("Why?", mation.seconds())

    why = mainlayer.Actor(mo.text.Text("Why?",
        pos=rim.last().bottom()-1j, align=[0,1],
        size=84, color=violet
        ))
    why.fadeIn(12, jump=-2j)

    mation.waitUntilSec(15.25)
    print("Scoot and show Euler's Formula:", mation.seconds())

    hexgrid.newendkey()
    imposs.newendkey()

    mo.action.move([rim, hexgrid], -2j, 20)
    mo.action.rollback([imposs, why], 20)

    mation.wait(5)

    euler = mainlayer.Actor(mo.latex.parse(r"e^{\violet{\theta i}} = \cos\violet\theta + \violet i \sin\violet\theta",
        pos=6j, boxHeight=1.25
        ))
    euler.fadeIn(15, jump=2j)

    mation.waitUntilSec(17.85)
    print("Crossout:", mation.seconds())

    cross = mainlayer.Actor(mo.gadgets.crossout(euler, pad=0.25,
        duration=15, width=7, color=red
        ))

    mation.waitUntilSec(18.65)
    print("Replace with characteristic formula:", mation.seconds())

    euler.newendkey()
    eulerchar = mainlayer.Actor(euler.last().dup().replaceTex(r"\dgreen V - \blue E + \red F = 2",
        gauge="="
        ))

    mo.action.fadeOut([euler, cross], 15, jump=-2j)
    eulerchar.fadeIn(15, jump=-2j)

    mation.waitUntilSec(21.8)
    print("Highlight vertices:", mation.seconds())

    pts = [z+radius*cmath.exp(n*tau/6*1j) for z in hexcenters for n in range(6)]
    pts = removeDuplicates(pts, key=lambda pt: cround(pt, 3))
    pts = [contortion(z) for z in pts]
    pts = [z for z in pts if abs(z) <= 5]
    pts.sort(key=lambda z: abs(z))
    pts = [mo.grid.Point(z).set(
        strokeWeight=2, color=black, fill=green
        ) for z in pts]
    pts = toplayer.Actor(mo.Frame(pts).set(
        origin=rim.last().origin
        ))

    eulerchar.newendkey(instant=True).select[0,2,4,-1].alignOrigin([0,0])
    eulerbase = eulerchar.last().dup()

    eulerchar.highlight(10, rescale=1.5, select=0)
    pts.subaction.popIn(8, substagger=0.25)

    mation.waitUntilSec(23)
    print("Highlight edges:", mation.seconds())

    eulerchar.newendkey()
    hexwarped = hexgrid.newendkey()
    pts.newendkey()

    eulerchar.newendkey(10, eulerchar.key[1].dup())
    eulerchar.highlight(0, rescale=1.5, select=2)

    def highlightEdges(actor, duration=10):
        actor.newendkey(duration).set(
            color=yellow, outlineWidth=2, outlineColor=black
            )
    hexgrid.subaction(highlightEdges, substagger=0.5,
        select=sorted(range(hexgrid.last().numfigs), key=lambda n: abs(hexgrid.last().figures[n].center()))
        )
    pts.subaction.popOut(10)

    mation.waitUntilSec(24.5)
    print("Highlight faces:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    eulerchar.newendkey()
    hexgrid.newendkey()

    eulerchar.newendkey(10, eulerchar.key[1].dup())
    eulerchar.highlight(0, rescale=1.5, select=4)

    def fillcolorGeneratorFunc():
        fills = [red, orange, yellow, green, blue, violet, white, (0.15,)*3]
        for n in range(1000):
            yield fills[n%len(fills)]
    fillcolor = fillcolorGeneratorFunc()
    def highlightFaces(actor, duration=10):
        actor.newendkey(duration).set(
            color=black, outlineWidth=0,
            fill=next(fillcolor), alphaFill=1
            )
    hexgrid.subaction(highlightFaces, substagger=0.5,
        select=sorted(range(hexgrid.last().numfigs), key=lambda n: abs(hexgrid.last().figures[n].center()))
        )

    mation.waitUntilSec(26)
    print("Restore and highlight '2':", mation.seconds())

    eulerchar.newendkey()
    hexgrid.newendkey()

    eulerchar.newendkey(10, eulerchar.key[1].dup())
    eulerchar.highlight(0, rescale=1.5, select=-1)

    hexgrid.newendkey(15, hexwarped.dup())

    mation.waitUntilSec(27.8)
    print("Label 'Euler Characteristic':", mation.seconds())

    eulerchar.newendkey()
    eulerchar.newendkey(10, eulerbase.dup())

    charboxer = mainlayer.Actor(mo.gadgets.enbox(eulerchar, pad=0.5,
        duration=20, width=5, color=red
        ))
    charlabel = mainlayer.Actor(mo.text.paragraphPhys("Euler\nCharacteristic",
        pos=charboxer.last().top()-0.5j, align=[0,-1],
        size=1, color=black, ybuf=0.8
        ))

    mation.wait(5)

    mo.action.move([eulerchar, charboxer], -1j, 15)
    charlabel.fadeIn(15, jump=2j)






    print("Animation length:", mation.seconds())
    mation.wait(3*30)

    # mation.finitizeDelays(30)

    # mation.screen = 1

    # mation.start = mation.lastID()
    mation.locatorLayer = mainlayer
    mation.clickRound = 2
    mation.clickCopy = True
    # mation.newFrameRate(10)
    # mation.play()

    # print(mation.windowShape)

    # Check that no bookmarks are active
    # assert (mation.firstID() if mation.start is None else mation.start) <= min([oo]+list(mation.delays.keys()))
    mation.rescale(1920/1080)
    mation.newFrameRate(60)
    mation.export("./01_hexball.mp4", scale=1)


main()


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

    # mation.waitUntilSec()
    print("Show hex ball:", mation.seconds())

    rim = mainlayer.Actor(mo.grid.ellipse(0,5, dTheta=4*deg).set(
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

    hexgrid = layer2.Actor(mo.combo.TFrame([hexbase.copy().set(origin=z) for z in hexcenters]))
    hexgrid.last().all.commitTransforms()
    hexgrid.last().select[::4].set(
        fill=black, alphaFill=0.85
        )

    ballmask = layer2.mask.Actor(rim.last().dup().set(
        width=0, fill=black,
        modifier=lambda self: self._updateFrom(rim.now(), common=True, ignore={"fill", "width"})
        ))

    mo.action.move([rim, hexgrid], -1j, 0)

    rim.popIn(15)

    mation.waitUntilSec(3.4)
    print("Show 'k-many' label:", mation.seconds())

    kmany = toplayer.Actor(mo.combo.figureGrid([mo.latex.parse(r"\text{$\redderorange k$-many}",
            boxHeight=1.25
        ),
        hexbase.copy().set(transform=mo.matrix.scale2d(0.85)).commitTransforms().set(
            fill=white, alphaFill=1
            )],
        pos=rim.last().top()+1+3.25j,
        width=3.5
        ))
    kmany.fadeIn(12, jump=2j)

    pointer = toplayer.Actor(mo.grid.arc(kmany.last().southeast()-0.25-0.25j, rim.last().top()+2.5-0.25j, angle=-60*deg).set(
        width=5, color=black, headSize=30
        ))
    pointer.growIn(12)

    mation.waitUntilSec(5.4)
    print("Scoot and show V and E:", mation.seconds())

    pointer.newendkey()
    rim.newendkey()
    hexgrid.newendkey()

    Vlabel = toplayer.Actor(kmany.last().figures[0].dup().replaceTex(r"k =", gauge="k").replaceTex(r"\dgreen V =",
        gauge="=", pos=kmany.last().left()-2.5j, align=[-1,0]
        ).alignOrigin([1,0]))
    Elabel = toplayer.Actor(Vlabel.last().dup().replaceTex(r"\blue E =",
        gauge="=", pos=Vlabel.last().pos-2j
        ))

    pointer.fadeOut(12)
    mo.action.move([rim, hexgrid], -4.5j, duration=22)
    mo.action.fadeIn([Vlabel, Elabel], 15, jump=2j, stagger=7)

    rim.last().transform = hexgrid.last().transform = mo.matrix.scale2d(0.75)

    mation.waitUntilSec(8.5)
    print("Flourish the hexagons:", mation.seconds())

    hexgrid.newendkey()

    def hexflourish(actor):
        orig = actor.last().copy()
        actor.newendkey(10).set(
            fill=yellow, alphaFill=1
            )
        actor.newendkey(10, orig)
    hexgrid.subaction(hexflourish,
        select=sorted(range(hexgrid.last().numfigs), key=lambda n: abs(hexgrid.last().figures[n].center())),
        substagger=0.5
        )

    mation.waitUntilSec(10.4)
    print("Show 6k:", mation.seconds())

    Vlabel.newendkey(instant=True).replaceTex(r"\dgreen V = 6\redderorange k",
        gauge="=", align=mo.GAUGE
        )
    Elabel.newendkey(instant=True).replaceTex(r"\blue E = 6\redderorange k",
        gauge="=", align=mo.GAUGE
        )

    mo.subaction.fadeIn([Vlabel, Elabel], 12, jump=2, select=sel[-2:], stagger=7)

    mation.waitUntilSec(14.6)
    print("Zoom in on an edge:", mation.seconds())

    mainlayer.camera.newendkey()
    layer2.camera.newendkey().set(
        modifier=lambda self: self.set(view=mainlayer.camera.now().view)
        )
    layer2.mask.camera.newendkey().set(
        modifier=layer2.camera.last().modifier
        )

    mainlayer.camera.newendkey(20).zoomIn(2, focus=(-0.06-3.54j))

    mation.waitUntilSec(15.8)

    edge = layer2.Actor(hexgrid.last().sub[25].all.set(
        start=1/6, end=2/6,
        color=cyan, width=0, outlineWidth=2, outlineColor=black,
        ))
    edge.newendkey(7).all.set(width=30, color=yellow)
    edge.newendkey(6).all.set(width=8, color=cyan)

    mation.waitUntilSec(17)
    print("Show the two bordering hexagons:", mation.seconds())

    hexgrid_orig = hexgrid.newendkey()
    hexgrid.newendkey(10).select[25, 26].set(
        fill=[1, 0.35, 0.35], alphaFill=1
        )

    mation.waitUntilSec(19.2)
    print("Show vertex:", mation.seconds())

    vertex = layer2.Actor(mo.grid.Point((-0.39-3.55j)).set(
        strokeWeight=2, color=black, fill=green, size=50
        ))
    vertex.popIn(7)
    vertex.newendkey(6).size = 15

    mation.waitUntilSec(20.15)
    print("Highlight final bordering hex:", mation.seconds())

    hexgrid.newendkey(instant=True)
    hexgrid.newendkey(10).select[19].set(
        fill=[1, 0.35, 0.35], alphaFill=1
        )

    mation.waitUntilSec(22.5)
    print("Divide out 2 and 3:", mation.seconds())

    Vlabel.newendkey(instant=True).replaceTex(r"\dgreen V = 6\redderorange k / 3",
        gauge="=", align=mo.GAUGE
        )
    Elabel.newendkey(instant=True).replaceTex(r"\blue E = 6\redderorange k / 2",
        gauge="=", align=mo.GAUGE
        )
    mo.subaction.fadeIn([Vlabel, Elabel], 12,
        jump=2j, select=sel[-2:], stagger=7
        )

    mation.waitUntilSec(25)
    print("Simplify:", mation.seconds())

    Vlabel.newendkey()
    Elabel.newendkey()

    Vlabel.newendkey(15).replaceTex(r"\dgreen V = 2\redderorange k",
        gauge="=", align=mo.GAUGE
        ).set(subpool=sel[-2])
    Elabel.newendkey(15).replaceTex(r"\blue E = 3\redderorange k",
        gauge="=", align=mo.GAUGE
        ).set(subpool=sel[-2])

    mation.waitUntilSec(28.9)
    print("Zoom back out, clean up:", mation.seconds())

    mainlayer.camera.newendkey()
    hexgrid.newendkey()
    vertex.newendkey()

    mainlayer.camera.newendkey(20, mainlayer.camera.key[-3].dup())
    hexgrid.newendkey(20, hexgrid_orig.dup())
    mo.action.fadeOut([vertex, edge], 20)

    mation.waitUntilSec(30)
    print("Show face count:", mation.seconds())

    Flabel = toplayer.Actor(Elabel.last().dup().replaceTex(r"\red F = \redderorange k",
        gauge="=", align=mo.GAUGE, pos=Elabel.last().pos-2j
        ))
    Flabel.fadeIn(12, jump=-2j)

    mation.waitUntilSec(31)
    print("Show Euler characteristic:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    kmany.newendkey()
    Vlabel.newendkey()

    kmany.fadeOut(12)
    mo.action.move([Vlabel, Elabel, Flabel], 3.5j, duration=12)

    mation.wait(5)

    combined = mo.combo.TFrame([Vlabel.last().dup(), Elabel.last().dup(), Flabel.last().dup()]).combine()
    combined = combined.sub[0,1,4,5,8,9,2,3,6,7,-1]
    combined.set(subpool=sel[-3, -1])

    tex = r"""
    \begin{aligned}
        \dgreen V - &\blue E + \red F \\
        &= 2\redderorange k - 3\redderorange k + \redderorange k
    \end{aligned}
    """
    result = toplayer.Actor(Vlabel.last().dup().replaceTex(tex,
        gauge="=", pos=Flabel.last().bottom().imag*1j-1.5j, align=[0,1]
        ))
    result.morphFrom(combined, duration=20)

    mation.waitUntilSec(35)
    print("Morph to 0:", mation.seconds())

    result.newendkey()

    tex = r"""
    \begin{aligned}
        \dgreen V - &\blue E + \red F \\
        &= 0
    \end{aligned}
    """
    result.newendkey(15).replaceTex(tex,
        gauge="=", align=mo.GAUGE
        ).set(subpool=-1)

    mation.waitUntilSec(36)
    print("Show contradiction:", mation.seconds())

    tex = r"""
    \begin{aligned}
        \dgreen V - &\blue E + \red F \\
        &= 0 \:\red{\neq 2}
    \end{aligned}
    """
    result.newendkey(3, instant=True).replaceTex(tex,
        gauge="=", align=mo.GAUGE
        ).set(subpool=[]).subalignOrigin([-1,0], select=sel[-3:])
    result.subaction.fadeIn(10, select=sel[-3:], jump=2)

    mation.wait(5)

    result.subaction.flourish(8, select=sel[-3:], rescale=1.75)

    mation.waitUntilSec(38.7)
    print("Fade all:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    mo.action.fadeOut([actor for layer in reversed(list(mation.layers)) for actor in layer.actors if actor.last().visible],
        15, jump=2j, stagger=3)





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
    mation.export("./02_proof.mp4", scale=1)


main()


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
from blockletters import blockWord, makeLogo

# Set default transition to quadease
morpho.transition.default = quadease
# Set default font to be the LaTeX font
morpho.text.defaultFont = "CMU serif"


def main():
    # Define layers here
    mainlayer = morpho.Layer(view=mo.video.view169())
    layer2 = mainlayer.copy()
    mation = morpho.Animation([layer2, mainlayer])
    mation.windowShape = (1920, 1080)
    mation.fullscreen = True
    mation.background = lavender

    layer2.camera.first().zoomIn(12).centerAt(0.5+0.4j)

    bgsettings = dict(background=white, backAlpha=0.5)

    # mation.wait(30)
    # print("Draw axes:", mation.seconds())

    def f_base(x):
        return (4*x**3-51*x**2+180*x)/35
    def f(x):
        return 0.9*f_base(7.5*x)/7.5+0.1
    def df(x, dx=0.001):
        return (f(x+dx)-f(x-dx))/(2*dx)

    axes = layer2.Actor(mo.grid.mathaxes(
        view=[-2.25,3.25,-2.25,1.25],
        width=8, color=black,
        tickLength=20,
        tickOffset=-0.25
        ).set(zdepth=1))
    # axes.growIn(30)

    rightWall = layer2.Actor(mo.grid.Path([1-1j, 1+1.25j]).set(
        width=6, color=black, alpha=0.5,
        dash=[20,15], zdepth=1
        ))

    graph = layer2.Actor(mo.graph.realgraph(f, 0, 1, steps=100).set(
        width=6, color=mygreen,
        outlineWidth=2, outlineColor=mation.background
        ))
    # graph.growIn(20)

    mation.waitUntilSec(0.8)
    print("Pick arbitrary x:", mation.seconds())

    xvalue = layer2.Actor(mo.latex.parse(r"x",
        pos=0, align=[0,3.5], boxHeight=0.05, fill=myred, alpha=0,
        width=-4, color=mation.background,
        zdepth=1
        ))

    marker = layer2.Actor(mo.grid.Arrow(-1j, -0.005j).set(
        width=0, headSize=30, color=black, zdepth=1,
        modifier=lambda self: self.set(origin=xvalue.now().pos, alpha=xvalue.now().alpha)
        ))

    xvalue.newendkey(18).set(pos=0.75, alpha=1)
    xvalue.newendkey(14).set(pos=0.3)
    xvalue.newendkey(11).set(pos=0.45)
    xvalue.last().all.alignOrigin([0,0])
    xvalue.flourish(10, rescale=1.75, select=None)

    mation.waitUntilSec(6.25)
    print("Flash graph:", mation.seconds())

    ygraph = layer2.Actor(graph.last().copy().set(
        start=0, end=0, color=yellow
        ))
    ygraph.newendkey(40).set(start=1, end=1, visible=False)
    ygraph.newendkey(-20).set(start=0.42, end=0.58)

    mation.waitUntilSec(8)
    print("Draw in graph point:", mation.seconds())

    altitude = layer2.Actor(mo.grid.Path().set(
        width=4, color=black, dash=[15],
        modifier=lambda self: self.set(seq=[0,1j*f(x := xvalue.now().pos)], origin=x)
        ))
    altitude.growIn(15)

    gpt = layer2.Actor(mo.grid.Point().set(
        strokeWeight=2, size=22, color=black, fill=goodblue,
        modifier=lambda self: self.set(pos=complex(xvalue.now().pos, f(xvalue.now().pos)))
        ))
    gpt.popIn(8)
    gpt.newendkey(6).size = 15

    mation.waitUntilSec(9)
    print("Wiggle x a little:", mation.seconds())

    xvalue.newendkey()
    x = xvalue.last().pos
    xvalue.newendkey(8).pos = 0.4
    xvalue.newendkey(12).pos = 0.5
    for n in range(4):
        xvalue.newendkey(12).pos = 0.4
        xvalue.newendkey(12).pos = 0.5
    xvalue.newendkey(8).pos = x

    mation.waitUntilSec(14.25)
    print("Draw delta bubble:", mation.seconds())

    dbubble = layer2.Actor(mo.shapes.roundedRect([0.4, 0.5, -0.01, 0.01], relative=True).set(
        width=2, color=black, fill=[1,0.25,0.25], alphaFill=1, zdepth=1
        ), beforeActor=marker)
    dbubble.newendkey(15)
    dbubble.first().set(transform=mo.matrix.scale2d(0,1))

    dcurtain = layer2.Actor(mo.grid.rect([0.4, 0.5, -1.5, 1.5], relative=True).set(
        width=0, fill=red, alpha=0.5, zdepth=-1
        ))
    dcurtain.newendkey(20)
    dcurtain.first().set(transform=mo.matrix.scale2d(1,0))

    mation.wait(20)
    print("Wiggle x around some more:", mation.seconds())

    xvalue.newendkey()
    x = xvalue.last().pos
    xvalue.newendkey(8).pos = 0.4
    xvalue.newendkey(12).pos = 0.5
    xvalue.newendkey(12).pos = 0.4
    xvalue.newendkey(12).pos = 0.5
    xvalue.newendkey(8).pos = x

    mation.waitUntilSec(18)
    print("'Delta interval':", mation.seconds())

    deltalabel = layer2.Actor(mo.latex.parse(r"\text{$\delta$-interval}",
        pos=x, align=[0,-1.75], boxHeight=0.07,
        background=mation.background, backAlpha=0.85, backPad=0.02
        ))
    deltalabel.last().select[0].set(fill=myred)
    deltalabel.fadeIn(15, jump=0.1j)

    mation.waitUntilSec(22.15)
    print("Draw in epsilon curtain:", mation.seconds())

    ebubble = layer2.Actor(mo.shapes.roundedRect([-0.01, 0.01, f(0.5), f(0.4)], relative=True).set(
        width=2, color=black, fill=[0.25,1,0.25], alphaFill=1, zdepth=1
        ), beforeActor=dbubble)
    ebubble.newendkey(15)
    ebubble.first().set(transform=mo.matrix.scale2d(1,0))

    ecurtain = layer2.Actor(mo.grid.rect([-2.5, 2.5, f(0.5), f(0.4)], relative=True).set(
        width=0, fill=[0,0.8,0], alpha=0.5, zdepth=-1
        ))
    ecurtain.newendkey(20)
    ecurtain.first().set(transform=mo.matrix.scale2d(0,1))

    mation.waitUntilSec(24.1)
    print("Zoom in and show epsilon-radius < 0.1:", mation.seconds())

    layer2.camera.newendkey()
    layer2.camera.newendkey(30).zoomIn(4).centerAt(complex(x, f(x)))

    deltalabel.newendkey().visible = False

    mation.wait(8)

    ymin = f(0.5)
    y = f(x)
    ymax = f(0.4)

    spanner = layer2.Actor(mo.Frame(
        upper=mo.grid.Arrow(y*1j, ymax*1j),
        lower=mo.grid.Arrow(y*1j, ymin*1j)
        ), beforeActor=gpt)
    spanner.last().all.set(
        origin=x,
        width=5, color=black, headSize=25,
        outlineWidth=2, outlineColor=mation.background
        )
    spanner.subaction.growIn(15)

    lesslabel1 = layer2.Actor(mo.text.Text("< 0.1",
        pos=spanner.last().upper.center(), align=[-1.1,0],
        size=56, color=black
        ).set(**bgsettings, backPad=0.002),
        beforeActor=spanner)
    lesslabel2 = layer2.Actor(lesslabel1.last().copy().set(
        pos=spanner.last().lower.center(), align=[1.1,0]
        ), beforeActor=spanner)

    lesslabel1.fadeIn(15, jump=lesslabel1.last().boxWidth()/2)
    lesslabel2.fadeIn(15, jump=-lesslabel1.last().boxWidth()/2)

    mation.waitUntilSec(28.35)
    print("Zoom back out:", mation.seconds())

    layer2.camera.newendkey()
    lesslabel2.newendkey()

    layer2.camera.newendkey(30, layer2.camera.first().copy())
    mo.action.rollback([spanner, lesslabel1, lesslabel2], 30)

    mation.waitUntilSec(30)
    print("Highlight delta interval:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    dbubble.newendkey()
    dcurtain.newendkey()

    dbubble.flourish(10, width=2, rescale=2)
    dbubble.last().fill = yellow
    dcurtain.newendkey(10).set(fill=yellow)

    mation.waitUntilSec(32.5)
    print("Highlight epsilon interval:", mation.seconds())

    dbubble.newendkey()
    dcurtain.newendkey()
    ebubble.newendkey()
    ecurtain.newendkey()

    dbubble.newendkey(10, dbubble.key[1].copy())
    dcurtain.newendkey(10, dcurtain.key[1].copy())
    ebubble.flourish(10, width=2, rescale=2)
    ebubble.last().fill = yellow
    ecurtain.newendkey(10).set(fill=yellow)

    mation.waitUntilSec(36.25)
    print("Label the epsilon curtain as bounded:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    bdd = layer2.Actor(mo.text.MultiText("Bounded",
        pos=complex(-0.3, y), align=[0,0],
        size=56, color=black
        ))
    bdd.newendkey(12)
    bdd.first().set(transform=mo.matrix.scale2d(1,0))

    mation.waitUntilSec(40.75)
    print("'Locally bounded':", mation.seconds())

    bdd.newendkey()
    ebubble.newendkey()
    ecurtain.newendkey()

    bdd.newendkey(20).set(
        text="Locally bounded",
        pos=complex(x, f(x))+0.12j, size=66,
        **bgsettings, backPad=0.033
        )
    ebubble.newendkey(20, ebubble.key[1].copy())
    ecurtain.newendkey(20, ecurtain.key[1].copy())

    mation.waitUntilSec(47)
    print("Slide the delta interval around:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    bdd.newendkey()
    bdd.fadeOut(15)

    @mo.SkitParameters(x=-1, radius=0.05, alpha=1)
    class EpsilonDeltaSystem(mo.Skit):
        def makeFrame(self):
            x = xvalue.now().pos.real if self.x < 0 else self.x
            radius = self.radius
            alpha = self.alpha

            dbubble = mo.shapes.roundedRect([x-radius, x+radius, -0.01, 0.01], relative=True).set(
                width=2, color=black, fill=[1,0.25,0.25], alphaFill=1,
                alpha=alpha
                )

            _, _, y1, y2 = graph.now()[x-radius:x+radius].box()

            ebubble = mo.shapes.roundedRect([-0.01, 0.01, y1, y2], relative=True).set(
                width=2, color=black, fill=[0.25,1,0.25], alphaFill=1,
                alpha=alpha
                )

            return mo.Frame(delta=dbubble, epsilon=ebubble)

    dbubble.newendkey().visible = False
    ebubble.newendkey().visible = False
    edsys = layer2.Actor(EpsilonDeltaSystem(radius=0.05).set(
        zdepth=1
        ), beforeActor=marker)

    def dcurtainModifier(self):
        x = xvalue.now().pos.real
        radius = edsys.now().radius

        rect = mo.grid.rect([x-radius, x+radius, -1.5, 1.5], relative=True)
        self.vertices = rect.vertices
        self.origin = rect.origin

    def ecurtainModifier(self):
        x = xvalue.now().pos.real
        radius = edsys.now().radius

        _, _, y1, y2 = graph.now()[x-radius:x+radius].box()

        rect = mo.grid.rect([-2.5, 2.5, y1, y2], relative=True)
        self.vertices = rect.vertices
        self.origin = rect.origin

    def radscale(x):
        return 1/max(1,abs(df(x)))

    dcurtain.newendkey().modifier = dcurtainModifier
    ecurtain.newendkey().modifier = ecurtainModifier
    xvalue.newendkey()
    edsys.newendkey().modifier = lambda self: self.set(radius=self.radius*radscale(xvalue.now().pos.real))

    xvalue.newendkey(45).pos = 0.1
    # edsys.newendkey(-20, glob=True)
    # edsys.newendkey().set(radius=0.012)
    mation.wait(15)
    xvalue.newendkey(75).pos = 0.9
    # edsys.newendkey(-30, glob=True).set(radius=0.05)
    # edsys.newendkey().set(radius=0.025)

    mation.waitUntilSec(53.5)
    print("Show infinite intervals:", mation.seconds())

    mo.action.fadeOut([xvalue, edsys, dcurtain, ecurtain, altitude, gpt], 18)

    dbubs = []
    ebubs = []
    for x in np.linspace(0.01, 0.99, 75).tolist():
        radius = 0.05*radscale(x)
        a = constrain(x-radius, 0, 1)
        b = constrain(x+radius, 0, 1)
        dbub = mo.shapes.roundedRect([a, b, -0.01, 0.01], relative=True).set(
            width=2, color=black, fill=[1,0.25,0.25], alphaFill=1,
            zdepth=radius
            )
        dbubs.append(dbub)


        _, _, y1, y2 = graph.last()[a:b].box()
        ebub = mo.shapes.roundedRect([-0.01, 0.01, y1, y2], relative=True).set(
            width=2, color=black, fill=[0.25,1,0.25], alphaFill=1,
            alpha=1, zdepth=0
            )
        ebubs.append(ebub)


    dfoam = layer2.Actor(mo.Frame(dbubs).set(zdepth=1))
    efoam = layer2.Actor(mo.Frame(ebubs).set(zdepth=1))

    mo.subaction.popIn([dfoam, efoam], 10, substagger=0.5)

    mation.waitUntilSec(minsec(1.0455))
    print("'Overcovered!':", mation.seconds())

    overcovered = layer2.Actor(mo.text.Text("Overcovered!",
        pos=0.5, align=[0,-2],
        size=66, color=myred
        ))
    overcovered.fadeIn(20, jump=0.1j)

    mation.waitUntilSec(minsec(1.0615))
    print("Reduce to finite subcover:", mation.seconds())

    overcovered.rollback(15)

    dfoam.newendkey()
    efoam.newendkey()

    selection = sel[10:-1:2, 10:-10:3, 20:-10:5, 21:-10:7, 35:55:11, 53]
    dfoam.subaction.fadeOut(20, jump=0.2j, select=selection, substagger=0.5)
    efoam.subaction.fadeOut(20, jump=-0.2, select=selection, substagger=0.5)

    mation.waitUntilSec(minsec(1.1075))
    print("Flash the finite subcover:", mation.seconds())

    dfoam.subaction.flourish(15, width=2, select=lambda bubble: bubble.visible)

    mation.waitUntilSec(minsec(1.1615))
    print("Move collection of epsilon bubbles:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    efoam.newendkey()
    efoam.newendkey(30)
    for n, (dbub, ebub) in enumerate(zip(dfoam.last().figures, efoam.last().figures)):
        if not dbub.visible: continue
        ebub.set(pos=dbub.pos-0.075j)

    allbdd = layer2.Actor(mo.text.Text("All bounded!",
        pos=0.5-0.2j,
        size=66, color=brown
        ))
    allbdd.fadeIn(20, jump=-0.2j)

    mation.waitUntilSec(minsec(1.2025))
    print("Restore epsilon bubbles:", mation.seconds())

    efoam.newendkey()

    efoam.newendkey(20, efoam.key[-3].copy())
    allbdd.fadeOut(20)

    mation.waitUntilSec(minsec(1.211))
    print("Highlight delta bubbles sequentially:", mation.seconds())

    dfoam.newendkey().set(tweenMethod=dfoam.figureType.tweenInstant)
    dfoam.subaction.flourish(2, width=2, zdepth=100, select=lambda bub: bub.visible, substagger=2)

    mation.waitUntilSec(minsec(1.2755))
    print("Highlight the maximizer:", mation.seconds())

    dfoam.newendkey().set(tweenMethod=dfoam.figureType.tweenLinear)
    efoam.newendkey()

    dfoam.newendkey(10).select[23].set(fill=yellow, zdepth=100)
    efoam.newendkey(10).select[23].set(fill=yellow, zdepth=100)

    a,b,_,_ = dfoam.last().sub[23].box()
    _,_,c,d = efoam.last().sub[23].box()

    mation.wait(15)
    print("Create curtains:", mation.seconds())

    dcurtain2 = layer2.Actor(mo.grid.rect([a, b, -1.5, 1.5], relative=True).set(
        width=0, fill=red, alpha=0.5, zdepth=-1
        ))
    ecurtain2 = layer2.Actor(mo.grid.rect([-2.5, 2.5, c, d], relative=True).set(
        width=0, fill=[0,0.8,0], alpha=0.5, zdepth=-1
        ), timeOffset=7)

    dcurtain2.newendkey(15)
    dcurtain2.first().set(transform=mo.matrix.scale2d(1,0))
    ecurtain2.newendkey(15)
    ecurtain2.first().set(transform=mo.matrix.scale2d(0,1))

    mation.wait(20)

    upperbound = layer2.Actor(mo.grid.Path([-1, 2]).set(
        width=4, color=redderorange, dash=[10], origin=d*1j
        ))
    upperbound.growIn(20)

    uppertext = layer2.Actor(mo.text.Text("Upperbound",
        pos=-0.02+d*1j, align=[1,-1.75],
        size=66, color=redderorange
        ))
    uppertext.fadeIn(15, jump=0.1j)

    mation.waitUntilSec(minsec(1.321))
    print("Fade critical bubbles and curtains:", mation.seconds())

    dcurtain2.newendkey()
    dfoam.newendkey()
    efoam.newendkey()

    mo.action.fadeOut([dcurtain2, ecurtain2], 20)
    dfoam.newendkey(20, dfoam.key[-3].copy())
    efoam.newendkey(20, efoam.key[-3].copy())

    mation.waitUntilSec(minsec(1.328))
    print("Show lowerbound:", mation.seconds())

    dfoam.newendkey()
    efoam.newendkey()

    dfoam.newendkey(15).select[0].set(fill=yellow, zdepth=100)
    efoam.newendkey(15).select[0].set(fill=yellow, zdepth=100)

    a,b,_,_ = dfoam.last().sub[0].box()
    _,_,c,d = efoam.last().sub[0].box()

    dcurtain3 = layer2.Actor(mo.grid.rect([a, b, -1.5, 1.5], relative=True).set(
        width=0, fill=red, alpha=0.5, zdepth=-1
        ))
    ecurtain3 = layer2.Actor(mo.grid.rect([-2.5, 2.5, c, d], relative=True).set(
        width=0, fill=[0,0.8,0], alpha=0.5, zdepth=-1
        ), timeOffset=7)

    dcurtain3.newendkey(15)
    dcurtain3.first().set(transform=mo.matrix.scale2d(1,0))
    ecurtain3.newendkey(15)
    ecurtain3.first().set(transform=mo.matrix.scale2d(0,1))

    lowerbound = layer2.Actor(mo.grid.Path([-1, 2]).set(
        width=4, color=violet, dash=[10], origin=c*1j
        ))
    lowerbound.growIn(20)

    lowertext = layer2.Actor(mo.text.Text("Lowerbound",
        pos=-0.02+c*1j, align=[1,1.25],
        size=66, color=violet
        ))
    lowertext.fadeIn(15, jump=-0.1j)

    mation.waitUntilSec(minsec(1.365))
    print("Fade all bubbles and show global curtain:", mation.seconds())

    # mation.start = mation.lastID()  # BOOKMARK

    dcurtain3.newendkey()
    dfoam.newendkey()

    mo.action.fadeOut([dcurtain3, ecurtain3], 20)
    mo.action.fadeOut([dfoam, efoam], 20)

    bigcurtain = layer2.Actor(mo.grid.rect([-1, 2, lowerbound.last().origin.imag, upperbound.last().origin.imag], relative=True).toPath().set(
        width=0, fill=goodblue, alpha=0.5, zdepth=-1
        ))
    bigcurtain.first().alignOrigin([-1,0])
    bigcurtain.newendkey(30)
    bigcurtain.first().set(transform=mo.matrix.scale2d(0,1))

    mation.waitUntilSec(minsec(1.409))
    print("Show delta-interval sliding again:", mation.seconds())

    xvalue.newendkey().set(pos=0.1).all.set(visible=True)
    mo.action.fadeIn([xvalue, edsys, dcurtain, ecurtain, altitude, gpt], 15)
    dcurtain.last().alpha = 0.5
    ecurtain.last().alpha = 0.5

    bigcurtain.fadeOut(15)

    mation.wait(10)

    xvalue.newendkey(45).set(pos=0.9)

    mation.waitUntilSec(minsec(1.438))
    print("Restore big curtain:", mation.seconds())

    bigcurtain.newendkey()

    bigcurtain.fadeIn(15, alpha=0.5)
    mo.action.fadeOut([xvalue, edsys, dcurtain, ecurtain, altitude, gpt], 15)





    print("Animation length:", mation.seconds())
    mation.wait(10*30)

    # mation.finitizeDelays(30)

    # mation.start = mation.lastID()
    mation.locatorLayer = layer2
    mation.clickRound = 2
    mation.clickCopy = True
    # mation.newFrameRate(10)
    mation.play()

    # mation.newFrameRate(8)
    # mation.export("./20_proof.mp4", scale=1/4)


main()

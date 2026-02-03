import morpholib as morpho
mo = morpho

from morpholib.text import Text, PText, space, underline
from morpholib.transitions import coast
from morpholib.gadgets import enbox, enboxFlourish, crossout, encircle
from morpholib.calculus import diff

import morpholib.latex

dash = "\u2012"
o = "\u2022"  # Bullet point symbol

mo.latex.cacheDir = "./tex"

morpho.latex.preamble += r"""
\usepackage{mathtools}  % math enhancements latex2e (replaces amstex)
\usepackage{amssymb}    % AMSFonts and symbols
\usepackage{bm}         % Allows for arbitrary bold symbols using the \bm{} command
\usepackage{eucal}      % Euler Cal/Script Fonts
\usepackage{latexsym}   % latex symbols (like \pounds)
\usepackage{mathdots}   % Contains \iddots which is rotated \ddots
\usepackage{nicefrac}   % \nicefrac is slanted \frac
\usepackage{relsize}    % Allows for arb math enlarging using \mathlarger{}

\newcommand{\grow}[1]{\mathlarger{#1}} \newcommand{\shrink}[1]{\mathsmaller{#1}}
\newcommand*{\stack}[2]{\genfrac{}{}{0pt}{}{#1}{#2}}  % \frac without the bar. See also \stackrel{}{}
\newcommand*{\nfrac}[2]{\nicefrac{#1}{#2}}  % Short for \nicefrac. Renders 1/2 more nicely.
\newcommand*{\sfrac}[2]{{}^{#1}\! /_{\! #2}}  % Slanted \frac. Renders 1/2 more nicely.
\newcommand{\half}{\tfrac 12}
\newcommand{\abs}{\operatorname{abs}}  % \operatorname*{} makes _ ^ act like \sum
\newcommand{\floor}[1]{\left\lfloor #1 \right\rfloor} \newcommand{\ceil}[1]{\left\lceil #1 \right\rceil} \newcommand{\Angle}[1]{\left\langle #1 \right\rangle}
\renewcommand{\Vec}[1]{\bm{\vec{\mathrm{#1}}}}
\renewcommand{\Hat}[1]{\bm{\hat{\mathrm{#1}}}}
\newcommand{\Ihat}{{\bm{\hat{\textnormal{\bfseries\i}}}}} \newcommand{\ihat}{\hat{\imath}}
\newcommand{\Jhat}{{\bm{\hat{\textnormal{\bfseries\j}}}}} \newcommand{\jhat}{\hat{\jmath}}
\newcommand{\Khat}{\mathbf{\hat k}} \newcommand{\khat}{\hat{k}}
\newcommand{\degs}{^\circ}
\renewcommand{\o}{\circ}
\newcommand{\udots}{\iddots}
\newcommand{\dec}{\searrow} \newcommand{\inc}{\nearrow}
\newcommand{\AND}{\textsc{ and }} \newcommand{\OR}{\textsc{ or }} \newcommand{\NOT}{\textsc{ not }} \newcommand{\NOR}{\textsc{ nor }}
\newcommand{\Implies}{\Rightarrow} \newcommand{\If}{\Leftarrow} \newcommand{\Iff}{\Leftrightarrow}
\newcommand{\Forall}[1]{\forall \: #1 \colon} \newcommand{\Exists}[1]{\exists \: #1 \colon} \newcommand{\Unique}[1]{\exists ! \: #1 \colon} \newcommand{\forsome}{\Finv}
\newcommand{\x}{\times}
\newcommand{\R}{\mathbb{R}} \newcommand{\C}{\mathbb{C}} \newcommand{\N}{\mathbb{N}} \newcommand{\Z}{\mathbb{Z}} \newcommand{\Q}{\mathbb{Q}}
\renewcommand{\O}{\varnothing}
\newcommand{\cut}{\setminus} \newcommand{\co}{^\mathrm{co}}
\newcommand{\dsjt}{\asymp} \newcommand{\hits}{\not \asymp}
\newcommand{\tri}{\operatorname{\triangle}}
\newcommand{\E}{\operatorname{\textsc{e}}}
\newcommand{\dash}{\textrm{-}}
\renewcommand{\Re}{\operatorname{Re}} \renewcommand{\Im}{\operatorname{Im}}
\renewcommand{\mod}{\: \mathrm{mod} \:}
\newcommand{\der}{\partial} \newcommand{\del}{\nabla}
\newcommand{\eps}{\varepsilon} \newcommand{\oo}{\infty}
\newcommand{\inv}{^{-1}} \newcommand{\T}{^\mathrm{T}} \newcommand{\Tr}{^\mathrm{Tr}}
\newcommand{\oT}{^{\text{\textcircled{\scalebox{0.85}{\raisebox{-0.9pt}{T}}}}}}
\newcommand{\wave}[1]{\widetilde{#1}}
\newcommand{\script}[1]{\mathcal{#1}} % also try \mathfrak{} & \mathscr{}
\newcommand{\disp}[1]{$\displaystyle{ #1 }$}
\newcommand{\bfootnote}[1]{$^[$\footnote{#1}$^]$}
\newcommand{\Maketitle}{\setlength{\droptitle}{-10ex} \maketitle}  % Higher \maketitle
\newcommand{\titlesub}[2]{\title{#1 \\ \textsmaller{\textsmaller{#2}}}}
\newcommand{\Hline}{\noindent\rule{\textwidth}{1pt}}
\newcommand{\dedent}{$\!\!\!\!\!\!\!\!\!$}

% "Closed" square root symbol with a hook at the end
\usepackage{letltxmacro}
\LetLtxMacro{\OldSqrt}{\sqrt}
\newcommand{\ClosedSqrt}[1][\hphantom{3}]{\def\DHLindex{#1}\mathpalette\DHLhksqrt}
\makeatletter
    \newcommand*\bold@name{bold}
    \def\DHLhksqrt#1#2{%
        \setbox0=\hbox{$#1\OldSqrt{#2\,}$}\dimen0=\ht0\relax%
        % 0.4 here controls hook length
        \advance\dimen0-0.4\ht0\relax% size of the added box is still 0.4 times ht0
        \setbox2=\hbox{\vrule height\ht0 depth -\dimen0}%
        {\hbox{$#1\expandafter\OldSqrt\expandafter[\DHLindex]{#2\,}$}
        \lower\ifx\math@version\bold@name0.6pt\else0.4pt\fi\box2}
    }
    % root index positioning and added space at the end, mostly noticeable in inline math mode
    \newcommand*{\Sqrt}[2][]{\,\ClosedSqrt[\leftroot{-2}\uproot{1}#1\,]{#2}\kern0.1em}
\makeatother

\definecolor{myred}{rgb}{0.8, 0, 0}
\definecolor{myblue}{rgb}{0, 0, 0.7}
\definecolor{mygreen}{rgb}{0, 0.7, 0}
\definecolor{darkgreen}{rgb}{0, 0.5, 0}
\definecolor{myorange}{HTML}{ff6300}
\definecolor{redorange}{HTML}{ff6600}
\definecolor{redderorange}{HTML}{ff4400}
\definecolor{lightviolet}{HTML}{ff8bff}
\definecolor{softblue}{HTML}{248bad}
\definecolor{goodblue}{rgb}{0, 0.375, 0.75}
\definecolor{ygreen}{HTML}{7ba328}
\definecolor{seagreen}{HTML}{2e8b57}
\definecolor{beet}{HTML}{80003a}
\definecolor{brown}{rgb}{0.5, 0.25, 0}

\newcommand{\red}[1]{\textcolor{myred}{#1}}
\newcommand{\green}[1]{\textcolor{mygreen}{#1}}
\newcommand{\dgreen}[1]{\textcolor{darkgreen}{#1}}
\newcommand{\blue}[1]{\textcolor{myblue}{#1}}
\newcommand{\violet}[1]{\textcolor{violet}{#1}}
\newcommand{\redorange}[1]{\textcolor{redorange}{#1}}
\newcommand{\redderorange}[1]{\textcolor{redderorange}{#1}}
\newcommand{\softblue}[1]{\textcolor{softblue}{#1}}
\newcommand{\goodblue}[1]{\textcolor{goodblue}{#1}}
\newcommand{\beet}[1]{\textcolor{beet}{#1}}
\newcommand{\brown}[1]{\textcolor{brown}{#1}}
\newcommand{\gray}[1]{\textcolor{gray}{#1}}
\newcommand{\darkgray}[1]{\textcolor{darkgray}{#1}}
\newcommand{\xsub}[1]{\textcolor{myred}{x}_{\textcolor{violet}{#1}}}
\newcommand{\ddx}{{\frac{d}{dx}}\:}


% Document-specific custom commands
\newcommand{\ox}{\otimes}
\newcommand{\tr}{\operatorname{tr}}
\newcommand{\mat}{\operatorname{mat}}
\newcommand{\lrangle}[1]{\left\langle #1 \right\rangle}
\newcommand{\Span}{\operatorname{span}}
"""

# # Changes default text color
# mo.latex.preamble += r"""
# \everydisplay{\color{red}}
# """

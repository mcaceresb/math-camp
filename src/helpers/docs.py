#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from textwrap import dedent
from pathlib import Path

import sys
import os

CWD  = Path(__file__).resolve().parent
ROOT = Path('.').resolve()
OUT  = ROOT / 'docs'
OUT.mkdir(parents = True, exist_ok = True)


def main():
    print(sys.version)
    print(sys.platform if 'win' in sys.platform else os.linesep.join(os.uname()))

    datestr = datetime.today().strftime("%H:%M %a %b %d, %Y")
    print(os.linesep.join(['-' * 72, datestr]))

    html = dedent("""
    If the PDF does not appear below, please download the file [here <img src="https://upload.wikimedia.org/wikipedia/commons/6/64/Icon_External_Link.png" width="13px"/>]({0}).

    <object data="{0}" type="application/pdf" width="100%"  style="height:100vh" >
        <embed src="{0}#pagemode=0&navpanes=0"></embed>
    </object>
    """)

    markdown = dedent("""
        The {0} will be posted {1} the {2} lecture.
    """)

    problems = [
        ('right before', 2, 'out/homework/Math Camp 2022 Problem Set 1.pdf'),
        ('right before', 4, 'out/homework/Math Camp 2022 Problem Set 2.pdf'),
        ('right before', 6, 'out/homework/Math Camp 2022 Problem Set 3.pdf')
    ]

    solutions = [
        ('right before', 4, 'out/homework/Math Camp 2022 Suggested Solutions 1.pdf'),
        ('right before', 6, 'out/homework/Math Camp 2022 Suggested Solutions 2.pdf'),
        ('a day after', 6, 'out/homework/Math Camp 2022 Suggested Solutions 3.pdf')
    ]

    lectures = [
        ('right after', 1, 'out/lectures/Math Camp 2022 Lecture 1 - Proofs, Metric Spaces, Topology.pdf'),
        ('right after', 2, 'out/lectures/Math Camp 2022 Lecture 2 - Sequences, Continuity.pdf'),
        ('right after', 3, 'out/lectures/Math Camp 2022 Lecture 3 - Compactness, EVT, Correspondences.pdf'),
        ('right after', 4, 'out/lectures/Math Camp 2022 Lecture 4 - Differentiation, IFT, Unconstrained Optimization.pdf'),
        ('right after', 5, 'out/lectures/Math Camp 2022 Lecture 5 - Constrained Optimization, Envelope Theorem, Integration.pdf'),
        ('right after', 6, 'out/lectures/Math Camp 2022 Lecture 6 - Linear Algebra, ODE.pdf')
    ]

    for i, (mkstub1, mkstub2, filepdf) in enumerate(problems):
        with open(OUT / f'problems/problem{i+1}.md', 'w') as md:
            if (OUT / filepdf).is_file():
                md.write(html.format('../' + filepdf.replace(' ', '%20')))
            else:
                md.write(markdown.format('problem set', mkstub1, ordinal(mkstub2)))

    for i, (mkstub1, mkstub2, filepdf) in enumerate(solutions):
        with open(OUT / f'solutions/solution{i+1}.md', 'w') as md:
            if (OUT / filepdf).is_file():
                md.write(html.format('../' + filepdf.replace(' ', '%20')))
            else:
                md.write(markdown.format('solutions', mkstub1, ordinal(mkstub2)))

    for i, (mkstub1, mkstub2, filepdf) in enumerate(lectures):
        with open(OUT / f'lectures/lecture{i+1}.md', 'w') as md:
            if (OUT / filepdf).is_file():
                md.write(html.format('../' + filepdf.replace(' ', '%20')))
            else:
                md.write(markdown.format('lecture notes', mkstub1, ordinal(mkstub2)))

    datestr = datetime.today().strftime("%H:%M %a %b %d, %Y")
    print(os.linesep.join(['-' * 72, datestr]))


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


if __name__ == "__main__":
    main()

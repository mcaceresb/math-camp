from pandas import isnull
from os import linesep
import numpy as np


def save_table(output, tag, M, fmt = "\t{0:.9f}"):
    M = np.array(M)
    with open(output, "a+") as fh:
        fh.write(f"<tab:{tag}>{linesep}")
        if len(M.shape) == 1:
            for m in M:
                if m is None or isnull(m):
                    fh.write('\t')
                else:
                    fh.write(fmt.format(m))

            fh.write(linesep)
        else:
            for i in range(M.shape[0]):
                for j in range(M.shape[1]):
                    m = M[i, j]
                    if m is None or isnull(m):
                        fh.write('\t')
                    else:
                        fh.write(fmt.format(m))

                fh.write(linesep)

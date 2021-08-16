from os import path, linesep
from pathlib import Path


def SymLink(target, source):
    out = Path(str(target)).absolute()
    src = Path(str(source)).absolute()
    out.unlink(missing_ok = True)
    out.symlink_to(path.relpath(src, out.parent))


def CheckTargets(target):
    notfound = [str(t) for t in target if not Path(str(t)).exists()]
    if len(notfound):
        if len(notfound) > 1:
            msg = "Targets not found after build:" + linesep
            for tpath in notfound:
                msg += f"\t{tpath}" + linesep
        else:
            msg = f"Target '{notfound[0]}' not found after build"

        # raise FileNotFoundError(msg)
        raise Exception(msg)

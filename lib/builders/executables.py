from textwrap import indent, dedent
from pathlib import Path
from shutil import which

import yaml
import os


EXE_FILE = Path(__file__).resolve().parents[1] / 'executables.yml'


def get_executables(efile = EXE_FILE, languages = [], warn = False):
    warn_languages = []
    with open(efile, 'r') as e:
        executables = yaml.safe_load(e)
        for lang in list(executables.keys()) + languages:
            ENV = f'CUSTOM_EXE_{lang.replace(" ", "_")}'.upper()
            if ENV in os.environ:
                executables[lang] = os.environ[ENV]

    for lang, program in executables.items():
        exe = get_executable_path(program)
        if exe:
            executables[lang] = exe
        else:
            warn_languages += [[lang, program]]

    if warn:
        print_executable_warnings(warn_languages)

    return {lang: quote_str(exe) for lang, exe in executables.items()}


def get_executable_path(program):
    exe_global = which(program)
    exe_local  = str(Path(program).expanduser().resolve())
    if exe_global:
        return exe_global
    elif os.access(exe_local, os.X_OK):
        return exe_local


def print_executable_warnings(warn_languages):
    if len(warn_languages):
        s    = "s" if len(warn_languages) > 1 else ""
        maxl = 0
        for lang, program in warn_languages:
            maxl = max(maxl, len(lang))

        fmt = f"%-{maxl + 1}s %s"
        warn_fmt = []
        for (lang, program) in warn_languages:
            warn_fmt += [fmt % (lang + ':', program)]

        warn = dedent(f"""
            WARNING: Executable{s} not found or not executable.

            %s
        """) % indent(os.linesep.join(warn_fmt), '    ')
        print(warn)


def quote_str(x, quotechar = '"', contains = None):
    not_quoted = not (x.startswith(quotechar) or x.endswith(quotechar))
    x_contains = True if contains is None else x.find(contains) >= 0
    return quotechar + x + quotechar if not_quoted and x_contains else x


defaults = get_executables()

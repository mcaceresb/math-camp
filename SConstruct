from os import environ, path
from lib.helpers import Logger

import lib.builders as builders
import sys

logger = Logger('SConstruct.log')
sys.stdout = logger
sys.stderr = logger
env = Environment(
    ENV = environ,
    BUILDERS = {
        'm':    Builder(action = builders.Matlab),
        'do':   Builder(action = builders.Stata),
        'sas':  Builder(action = builders.SAS),
        'r':    Builder(action = builders.R),
        'py':   Builder(action = builders.Python),
        'link': Builder(action = builders.Link),
        'tablefill': Builder(action = builders.Tablefill)
    }
)

env['ENV']['TEXMFHOME'] = path.join(environ['HOME'], 'texmf')

Export('env')

# NB: This seems like a good idea but it's not.
# env.link(target = ['#docs/index.md'], source = ['#README.md'])

SConscript('src/syllabus/SConscript')
SConscript('src/lectures/SConscript')
SConscript('src/homework/SConscript')
SConscript('src/helpers/SConscript')

from tablefill import tablefill
from os import system, environ
from pathlib import Path
from hashlib import sha1
from shutil import copy

from .executables import defaults as executables
from .common import CheckTargets, SymLink


class CustomSconsBuilder(object):
    def __init__(self, target, source, env, log_action = None, ignore_errors = False):
        self.spath, self.login, self.logout = get_log_path(source[0])
        self.target = target

        self.log_action    = log_action
        self.ignore_errors = ignore_errors

    def make_system_call(self, lang, exe_args = '', executables = executables):
        ENV = f'CL_ARGS_{lang.replace(" ", "_")}'.upper()
        if ENV in environ:
            cl_args = environ[ENV]
        else:
            cl_args = ''

        exe  = executables[lang]
        call = f'{exe} {exe_args} "{self.spath}" {cl_args}'
        if self.log_action == 'redirect':
            call += f' > "{self.logout}" 2>&1'
        elif self.log_action == 'arg':
            call += f' "{self.logout}"'

        self.system_call = call

    def execute_system_call(self):
        print(self.system_call)
        rc = system(self.system_call)

        if rc and not self.ignore_errors:
            msg = f"System called exited with non-zero exit status {rc}"
            raise Warning(msg)

        self.cleanup()

    def cleanup(self):
        if self.log_action == 'move' and self.login.is_file():
            self.login.rename(self.logout)

        CheckTargets(self.target)


def get_log_path(source):
    spath  = Path(str(source))
    login  = Path(spath.name).with_suffix('.log')
    logout = Path('out').joinpath(*spath.parts[1:]).with_suffix('.log')
    return spath, login, logout


def Matlab(target, source, env):
    kwargs  = {} if 'KWARGS' not in env else env['KWARGS']
    builder = CustomSconsBuilder(target, source, env, **kwargs)
    digest  = sha1(builder.spath.encode()).hexdigest()

    copy(builder.spath, f"{digest}.m")
    builder.spath = f"""
        diary('{builder.logout}');
        addpath('{builder.spath.parent}');
        try,
            run('{digest}.m'),
        catch me,
            fprintf('%s: %s\\n', me.identifier, me.message),
            delete('{digest}.m'),
            exit(1),
        end,
        delete('{digest}.m');
        exit(0);
    """.replace('\n', ' ').replace('\r', ' ')

    builder.make_system_call('matlab', '-nodisplay -nosplash -nodesktop -r')
    builder.execute_system_call()


def Python(target, source, env):
    kwargs = {} if 'KWARGS' not in env else env['KWARGS']
    print(kwargs)
    if 'log_action' not in kwargs:
        kwargs['log_action'] = 'redirect'

    builder = CustomSconsBuilder(target, source, env, **kwargs)
    builder.make_system_call('python')
    builder.execute_system_call()


def Stata(target, source, env):
    kwargs = {} if 'KWARGS' not in env else env['KWARGS']
    if 'log_action' not in kwargs:
        kwargs['log_action'] = 'move'

    builder = CustomSconsBuilder(target, source, env, **kwargs)
    builder.make_system_call('stata', '-b do')
    builder.execute_system_call()


def SAS(target, source, env):
    kwargs = {} if 'KWARGS' not in env else env['KWARGS']
    if 'log_action' not in kwargs:
        kwargs['log_action'] = 'move'

    builder = CustomSconsBuilder(target, source, env, **kwargs)
    builder.make_system_call('sas')
    builder.execute_system_call()


def R(target, source, env):
    kwargs = {} if 'KWARGS' not in env else env['KWARGS']
    if 'log_action' not in kwargs:
        kwargs['log_action'] = 'redirect'

    builder = CustomSconsBuilder(target, source, env, **kwargs)
    builder.make_system_call('r',  '--no-save --no-restore --verbose')
    builder.execute_system_call()


def Link(target, source, env):
    for out, src in zip(target, source):
        SymLink(out, src)

    CheckTargets(target)


def Tablefill(target, source, env):
    kwargs = {} if 'KWARGS' not in env else env['KWARGS']
    spath  = str(source[0])
    input  = ' '.join(f'{s}' for s in source[1:])
    logout = get_log_path(source[0])[-1]
    logout = logout.with_stem(logout.stem + '_tablefill')

    if 'log_file' not in kwargs:
        kwargs['log_file'] = logout

    if 'log_only' not in kwargs:
        kwargs['log_only'] = True

    tablefill(template = spath,
              input    = input,
              output   = str(target[0]),
              verbose  = True,
              **kwargs)

    CheckTargets(target)

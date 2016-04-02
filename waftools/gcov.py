#! /usr/bin/env python
# encoding: utf-8
from waflib import Task, Options, Utils, Errors
from waflib.TaskGen import extension, feature, after_method
import os

from tempfile import NamedTemporaryFile

from contextlib import contextmanager

@contextmanager
def Wrapper(script):
    wrapper = NamedTemporaryFile(delete=False)
    wrapper.write(script)
    wrapper.close()
    os.chmod(wrapper.name, 0777)

    yield wrapper.name

    os.unlink(wrapper.name)

class gcov(Task.Task):
    color='PINK'
    after=['vnum', 'inst', 'tut']

    def keyword(self):
        return "Coverage"

    def run(self):
        # gcovr expects a single executable, but invoking llvm-cov requires
        # running "llvm-cov gcov ..." shell command
        wrapper_script = "#!/bin/sh\n{GCOV} {FLAGS} $*".format(
            GCOV="".join(self.env.GCOV),
            FLAGS="".join(self.env.GCOV_FLAGS))

        with Wrapper(wrapper_script) as wrapper:
            args = ['--gcov-executable=%s' % wrapper, '-r', self.srcnode.abspath()]
            proc = Utils.subprocess.Popen(self.env.GCOVR + args)
            proc.communicate()
            if proc.returncode != 0:
                raise Errors.WafError("Test %s failed" % self)

    def runnable_status(self):
        if Options.options.coverage:
            ret=super(gcov, self).runnable_status()
            return Task.RUN_ME if ret == Task.SKIP_ME else ret
        return Task.SKIP_ME

@after_method('apply_tut')
@feature('gcov')
def apply_gcov(self):
    if self.bld.options.coverage and not self.env.GCOVR:
        raise Errors.WafError('The project was not configured for gcov:'
                              'run ./waf configure --coverage first')

    task = self.create_task('gcov', self.link_task.outputs)
    task.srcnode = self.bld.srcnode

def options(opt):
    gr = opt.add_option_group('coverage options')
    gr.add_option('--coverage', action='store_true', default=False,
                  help='Show gcov coverage report when running tests')

def configure(cnf):
    if cnf.options.coverage:
        if cnf.options.check_cxx_compiler == 'clang++':
            cnf.find_program('llvm-cov', var='GCOV', mandatory=False)
            cnf.env.GCOV_FLAGS += ['gcov']
        else:
            cnf.find_program('gcov', var='GCOV', mandatory=False)

        cnf.find_program('gcovr', var='GCOVR', mandatory=False)
        cnf.check_cc(
            lib='gcov',
            uselib_store='GCOV'
        )
        cnf.env.CXXFLAGS += ['--coverage']
        cnf.env.LINKFLAGS += ['--coverage']

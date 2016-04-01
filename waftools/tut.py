#! /usr/bin/env python
# encoding: utf-8
from waflib import Task, Options, Logs, Utils, Errors
from waflib.TaskGen import feature, after_method
import os

class tut(Task.Task):
    color='PINK'
    after=['vnum', 'inst']

    def keyword(self):
        return "Executing"

    def run(self):
        env = os.environ.copy()
        env.update(self.environ)
        # TODO: add LD_LIBRARY_PATH to the env if project uses shared libs

        command = [self.inputs[0].abspath()]
        cwd = self.inputs[0].parent.abspath()
        proc = Utils.subprocess.Popen(command + self.args, cwd=cwd, env=env)
        proc.communicate()
        if proc.returncode != 0:
            raise Errors.WafError("Test %s failed" % self)

    def runnable_status(self):
        if Options.options.test:
            ret=super(tut, self).runnable_status()
            return Task.RUN_ME if ret == Task.SKIP_ME else ret
        return Task.SKIP_ME

@after_method('apply_link')
@feature('tut')
def apply_tut(self):
    task = self.create_task('tut', self.link_task.outputs)
    task.args = getattr(self, 'args', [])
    task.environ = getattr(self, 'environ', {})

def options(opt):
    gr = opt.add_option_group('test options')
    gr.add_option('--test', action='store_true', default=False,
                  help='Configure project to enable unit tests')

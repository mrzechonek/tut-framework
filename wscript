
APPNAME='tut'
VERSION='trunk'
srcdir = ''
blddir = 'build'

import Options
import Utils
import glob

def set_options(opt):
    opt.tool_options('compiler_cxx')
    opt.add_option('--debug', action='store_true', help='Build debug variant', default=False)

def configure(conf):
    conf.check_tool('g++')

    conf.env.PLATFORM = Utils.unversioned_sys_platform()
    conf.env.CPPFLAGS = [ '-O2', '-Wall', '-Wextra', '-Weffc++', '-Werror', '-ftemplate-depth-100' ]

    if Options.options.debug:
        conf.env.CPPFLAGS += [ '-O0', '-g' ]
        conf.env.set_variant('debug')

    conf.write_config_header('include/tut_config.h')

    print 'Configured for', conf.env.variant(), 'on', conf.env.PLATFORM

def build(bld):
    libtut = bld.new_task_gen(features='cxx', export_incdirs = 'include', target='tut')

    selftest = bld.new_task_gen(features='cxx cprogram', target='self_test', includes='.',
                                uselib_local = 'tut',
                                source = glob.glob('selftest/*.cpp'))

APPNAME='tut'
VERSION='2016-04-01'
srcdir = '.'
blddir = 'build'

from waflib import Options, Scripting, Utils, Build
import glob
import os

def options(opt):
    opt.load('compiler_cxx')
    opt.load('tut gcov', tooldir='waftools')

    gr = opt.add_option_group('build options')
    gr.add_option('--debug',      action='store_true', help='Build debug variant', default=False)

    gr.add_option('--with-rtti',    action='store_true', help='Enable RTTI (autodetect by default)', default=None)
    gr.add_option('--without-rtti', action='store_false', dest='with_rtti')

    gr.add_option('--with-seh',    action='store_true', help='Build with SEH extensions for win32 (off by default)', default=False)
    gr.add_option('--without-seh', action='store_false', dest='with_seh')

    gr.add_option('--with-posix',    action='store_true', help='Build with POSIX extensions (autodetect by default)', default=None)
    gr.add_option('--without-posix', action='store_false', dest='with_posix')

def configure(cnf):
    cnf.start_msg('Set installation prefix to')
    cnf.end_msg(cnf.env.PREFIX)

    cnf.load('compiler_cxx')
    cnf.load('tut gcov', tooldir='waftools')

    cnf.env.PLATFORM = Utils.unversioned_sys_platform()

    if cnf.env.COMPILER_CXX == 'g++':
        cnf.env.CPPFLAGS += [ '-O2', '-Wall', '-Wextra', '-Weffc++', '-ftemplate-depth-100' ]
        if cnf.options.debug:
            cnf.env.CPPFLAGS += [ '-O0', '-g' ]

    if cnf.env.COMPILER_CXX == 'msvc':
        if cnf.options.coverage:
            raise WafError('Self-test coverage is not available under msvc, sorry!')
            cnf.options.debug = True

        cnf.env.CPPFLAGS += [ '/DNOMINMAX' ]

    if cnf.options.with_posix is None:
        cnf.options.with_posix = cnf.check_cxx(fragment='#include <unistd.h>\nint main() { fork(); }',
                                               msg='Checking for fork()', mandatory=False)

    if cnf.options.with_rtti is None:
        cnf.options.with_rtti = cnf.check_cxx(fragment='#include <typeinfo>\nint main() { typeid(int).name(); }',
                                               msg='Checking for typeid()', mandatory=False)

    if cnf.options.with_posix:
        cnf.define_cond('TUT_USE_POSIX', 1)

    if cnf.options.with_seh:
        cnf.define_cond('TUT_USE_SEH', 1)

    if cnf.options.with_rtti:
        cnf.define_cond('TUT_USE_RTTI', 1)

    cnf.start_msg('Platform')
    cnf.end_msg(Utils.unversioned_sys_platform())

    def enabled_msg(msg, enabled):
        cnf.start_msg(msg)
        if enabled:
            cnf.end_msg('enabled')
        else:
            cnf.end_msg('disabled', color='YELLOW')

    enabled_msg('POSIX extensions', cnf.is_defined('TUT_USE_POSIX'))
    enabled_msg('Win32 structured exception handling', cnf.is_defined('TUT_USE_SEH'))
    enabled_msg('C++ run-time type identification', cnf.is_defined('TUT_USE_RTTI'))

    cnf.write_config_header( os.path.join('include', 'tut', 'tut_config.hpp') )


def build(bld):
    bld(features='cxx',
        includes='include',
        export_includes = 'include',
        target='tut')

    bld.install_files( os.path.join('${PREFIX}', 'include', 'tut'),
                       glob.glob(os.path.join('include', 'tut', '*.hpp')) )

    bld.install_files( os.path.join('${PREFIX}', 'include', 'tut'),
                       bld.env[Build.CFG_FILES])

    bld(features='cxx cprogram tut gcov',
        target='self_test',
        use='tut',
        source=glob.glob('selftest/*.cpp'),
        install_path=None)

    def write_pkgconfig(task):
        with open(task.outputs[0].abspath(), 'w') as f:
            f.write(
                '# tut.pc -- pkg-config data for Template Unit Test framework\n'
                'prefix=%(prefix)s\n'
                'INSTALL_BIN=${prefix}/bin\n'
                'INSTALL_INC=${prefix}/include\n'
                'INSTALL_LIB=${prefix}/lib\n'
                'exec_prefix=${prefix}\n'
                'libdir=${exec_prefix}/lib\n'
                'includedir=${prefix}/include\n'
                'Name: TUT\n'
                'Description: Template Unit Test framework\n'
                'Version: %(version)s\n'
                'Requires:\n'
                'Cflags: -I${includedir}\n' % dict(prefix=bld.options.destdir, version=VERSION))

    bld(target='tut.pc',
        rule=write_pkgconfig,
        install_path=os.path.join('${PREFIX}', 'lib', 'pkgconfig'))

    for example in ('simple', 'basic', 'shared_ptr', 'restartable'):
        bld(features='cxx cprogram',
            target='example_%s' % example,
            use='tut',
            source=glob.glob('examples/%s/*.cpp' % example),
            install_path=None)


def test(tst):
    Options.options.test = True
    Scripting.run_command('build')

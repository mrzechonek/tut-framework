
APPNAME='tut'
VERSION='trunk'
srcdir = ''
blddir = 'build'

import Options
import Utils
import glob
import os

def set_options(opt):
    opt.tool_options('compiler_cxx')
    opt.add_option('--debug',      action='store_true', help='Build debug variant', default=False)
    opt.add_option('--with-rtti',  action='store', help='Enable RTTI (on by default)', default=True)
    opt.add_option('--with-seh',   action='store', help='Build with SEH extensions for win32 (off by default)', default=False)
    opt.add_option('--with-posix', action='store', help='Build with POSIX extensions (off by default)', default=False)

    if Utils.unversioned_sys_platform() == 'win32':
        opt.add_option('--toolset',  action='store', help='Force compiler toolset (default is msvc)', default='msvc')
    else:
        opt.add_option('--toolset',  action='store', help='Force compiler toolset (default is g++)', default='g++')

    global trues
    trues = ('TRUE', 'True', 'true', 'ON', 'On', 'on', '1', True)

    opt.add_option('--test', action='store_true', help='Run self-tests after the build (off by default)', default=False)
def configure(conf):

    if Options.options.debug:
        conf.env.set_variant('debug')

    conf.env.PLATFORM = Utils.unversioned_sys_platform()

    conf.check_tool(Options.options.toolset)

    if Options.options.toolset == 'g++':
        conf.env.CPPFLAGS = [ '-O2', '-Wall', '-Wextra', '-Weffc++', '-Werror', '-ftemplate-depth-100' ]
        if Options.options.debug:
            conf.env.CPPFLAGS += [ '-O0', '-g' ]

    global trues

    if Options.options.with_posix in trues:
        conf.define_cond('TUT_USE_POSIX', 1)

    if Options.options.with_seh in trues:
        conf.define_cond('TUT_USE_SEH', 1)

    if Options.options.with_rtti in trues:
        conf.define_cond('TUT_USE_RTTI', 1)

    print 
    print 'Configured for %s, variant %s, using toolset %s' % ( Utils.unversioned_sys_platform(), conf.env.variant(), Options.options.toolset )
    print '    Installation directory                   : ', conf.env.PREFIX
    print '    POSIX extensions                         : ', conf.is_defined('TUT_USE_POSIX')
    print '    Win32 structured exception handling (SEH): ', conf.is_defined('TUT_USE_SEH')
    print '    C++ run-time type identification (RTTI)  : ', conf.is_defined('TUT_USE_RTTI')
    print 

    conf.write_config_header( os.path.join('include', 'tut', 'tut_config.hpp') )

    full=os.path.join( conf.blddir, conf.env.variant(), 'lib', 'pkgconfig', 'tut.pc' )
    full=os.path.normpath(full)
    (dir,base) = os.path.split(full)
    try:os.makedirs(dir)
    except:pass
    dest=open(full, 'w')
    dest.write('# tut.pc -- pkg-config data for Template Unit Test framework\n')
    dest.write('prefix='+conf.env.PREFIX+'\n')
    dest.write('INSTALL_BIN=${prefix}/bin\n')
    dest.write('INSTALL_INC=${prefix}/include\n')
    dest.write('INSTALL_LIB=${prefix}/lib\n')
    dest.write('exec_prefix=${prefix}\n')
    dest.write('libdir=${exec_prefix}/lib\n')
    dest.write('includedir=${prefix}/include\n')
    dest.write('Name: TUT\n')
    dest.write('Description: Template Unit Test framework\n')
    dest.write('Version: '+VERSION+'\n')
    dest.write('Requires:\n')
    dest.write('Cflags: -I${includedir}\n')
    dest.close()

def test(bld):
    if Options.options.test:
        cmd = os.path.join(bld.bdir, bld.env.variant(), 'self_test') + " -x"
        Utils.exec_command(cmd)

def build(bld):
    bld.add_post_fun(test)

    libtut = bld.new_task_gen(features='cxx', includes='include', export_incdirs = 'include', target='tut')
    # old headers
    bld.install_files( os.path.join('${PREFIX}', 'include'),
                       glob.glob(os.path.join('include','*.h')) )
    # new headers
    bld.install_files( os.path.join('${PREFIX}', 'include', 'tut'),
                       glob.glob(os.path.join('include', 'tut', '*.hpp')) )
    # config file
    bld.install_files( os.path.join('${PREFIX}', 'include', 'tut'),
                       os.path.join(bld.bdir, bld.env.variant(), 'include', 'tut', 'tut_config.hpp'))
    # pkgconfig file
    bld.install_files( os.path.join('${PREFIX}', 'lib', 'pkgconfig'),
                       os.path.join(bld.bdir, bld.env.variant(), 'lib', 'pkgconfig', 'tut.pc'))


    selftest = bld.new_task_gen(features='cxx cprogram', target='self_test',
                                uselib_local = 'tut',
                                install_path = None,
                                source = glob.glob('selftest/*.cpp'))

    ex_simple = bld.new_task_gen(features='cxx cprogram', target='example_simple',
                                 uselib_local = 'tut',
                                 install_path = None,
                                 source = 'examples/simple.cpp')

    ex_basic = bld.new_task_gen(features='cxx cprogram', target='example_basic',
                                uselib_local = 'tut',
                                install_path = None,
                                source = glob.glob('examples/basic/*.cpp'))

    ex_sharedptr = bld.new_task_gen(features='cxx cprogram', target='example_sharedptr', includes='.',
                                    uselib_local = 'tut',
                                    install_path = None,
                                    source = glob.glob('examples/shared_ptr/*.cpp'))

    ex_restartable = bld.new_task_gen(features='cxx cprogram', target='example_restartable',
                                      uselib_local = 'tut',
                                      install_path = None,
                                      source = glob.glob('examples/restartable/*.cpp'))


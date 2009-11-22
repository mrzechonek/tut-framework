#include <tut/tut.hpp>
#include <tut/tut_console_reporter.hpp>
#include <tut/tut_xml_reporter.hpp>

#include <exception>
#include <iostream>

namespace tut
{

    struct test
    {
        virtual ~test()
        {
        }
    };

    typedef test_group<test> tf;
    typedef tf::object object;
    tf fail_test("test()");

    template<>
    template<>
    void object::test<1>()
    {
        set_test_name("foo");
        skip();
    }


    test_runner_singleton runner;
}

int main()
{
    using namespace std;
    tut::console_reporter reporter;
    tut::xml_reporter xml_reporter;
    tut::callback *callback = &reporter;

    try
    {
        tut::runner.get().set_callback(callback);
        tut::runner.get().run_tests();
    }
    catch (const std::exception& ex)
    {
        cerr << "tut raised ex: " << ex.what() << endl;
        return 1;
    }
    catch( ... )
    {
        cerr << "tut raised unknown exception" << endl;
        return 1;
    }

    return !callback->all_ok();
}

#include <tut/tut.hpp>
#include <tut/tut_console_reporter.hpp>
#include <tut/tut_main.hpp>

#include <iostream>

namespace tut
{
    test_runner_singleton runner;
}

int main(int argc, char *argv[])
{
    tut::console_reporter reporter;
    tut::runner.get().set_callback(&reporter);

    try
    {
        if(tut::tut_main(argc, argv))
        {
            if(reporter.all_ok())
            {
                return 0;
            }
            else
            {
                std::cerr << std::endl;
                std::cerr << "*********************************************************" << std::endl;
                std::cerr << "WARNING: THIS VERSION OF TUT IS UNUSABLE DUE TO ERRORS!!!" << std::endl;
                std::cerr << "*********************************************************" << std::endl;
            }
        }
    }
    catch(const tut::no_such_group &ex)
    {
        std::cerr << "No such group: " << ex.what() << std::endl;
    }
    catch(const tut::no_such_test &ex)
    {
        std::cerr << "No such test: " << ex.what() << std::endl;
    }
    catch(const tut::tut_error &ex)
    {
        std::cout << "General error: " << ex.what() << std::endl;
    }

    return -1;
}

#include <tut/tut.hpp>
#include <tut/tut_cppunit_reporter.hpp>
#include <sstream>

using std::stringstream;

namespace tut
{

/**
 * Testing reporter.
 */
struct cppunit_reporter_test
{
    test_result tr1;
    test_result tr2;
    test_result tr3;
    test_result tr4;
    test_result tr5;
    test_result tr6;

    cppunit_reporter_test()
        : tr1("foo", 1, "", test_result::ok),
          tr2("foo", 2, "", test_result::fail),
          tr3("foo", 3, "", test_result::ex),
          tr4("foo", 4, "", test_result::warn),
          tr5("foo", 5, "", test_result::term),
          tr6("foo", 6, "", test_result::skipped)
    {
    }

    virtual ~cppunit_reporter_test()
    {
    }
};

typedef test_group<cppunit_reporter_test> tg;
typedef tg::object object;
tg cppunit_reporter_test("cppunit reporter");

template<>
template<>
void object::test<1>()
{
    skip();
}

template<>
template<>
void object::test<2>()
{
    skip();
#if 0
    std::stringstream ss;
    cppunit_reporter repo(ss);

    ensure_equals("ok count", repo.ok_count, 0);
    ensure_equals("fail count", repo.failures_count, 0);
    ensure_equals("ex count", repo.exceptions_count, 0);
    ensure_equals("warn count", repo.warnings_count, 0);
    ensure_equals("term count", repo.terminations_count, 0);

    repo.run_started();
    repo.test_completed(tr1);
    repo.test_completed(tr2);
    repo.test_completed(tr2);
    repo.test_completed(tr3);
    repo.test_completed(tr3);
    repo.test_completed(tr3);
    repo.test_completed(tr4);
    repo.test_completed(tr4);
    repo.test_completed(tr4);
    repo.test_completed(tr4);
    repo.test_completed(tr5);
    repo.test_completed(tr5);
    repo.test_completed(tr5);
    repo.test_completed(tr5);
    repo.test_completed(tr5);
    repo.test_completed(tr6);
    repo.test_completed(tr6);
    repo.test_completed(tr6);
    repo.test_completed(tr6);
    repo.test_completed(tr6);
    repo.test_completed(tr6);

    ensure_equals("ok count", repo.ok_count, 1+6); // 'skipped' means 'ok'
    ensure_equals("fail count", repo.failures_count, 2);
    ensure_equals("ex count", repo.exceptions_count, 3);
    ensure_equals("warn count", repo.warnings_count, 4);
    ensure_equals("term count", repo.terminations_count, 5);
    ensure(!repo.all_ok());
#endif
}

template<>
template<>
void object::test<3>()
{
    skip();
#if 0
    std::stringstream ss;
    cppunit_reporter repo(ss);

    repo.run_started();
    repo.test_completed(tr1);

    ensure_equals("ok count",repo.ok_count,1);
    ensure(repo.all_ok());

    repo.run_started();
    ensure_equals("ok count",repo.ok_count,0);
#endif
}

template<>
template<>
void object::test<4>()
{
    skip();
#if 0
    std::stringstream ss;
    cppunit_reporter repo(ss);

    repo.run_started();
    repo.test_completed(tr1);
    ensure(repo.all_ok());

    repo.run_started();
    repo.test_completed(tr1);
    repo.test_completed(tr2);
    ensure(!repo.all_ok());

    repo.run_started();
    repo.test_completed(tr3);
    repo.test_completed(tr1);
    ensure(!repo.all_ok());

    repo.run_started();
    repo.test_completed(tr1);
    repo.test_completed(tr4);
    ensure(!repo.all_ok());

    repo.run_started();
    repo.test_completed(tr5);
    repo.test_completed(tr1);
    ensure(!repo.all_ok());

    repo.run_started();
    repo.test_completed(tr1);
    repo.test_completed(tr6);
    ensure(repo.all_ok());
#endif
}

}


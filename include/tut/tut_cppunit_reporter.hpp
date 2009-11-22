
#ifndef TUT_CPPUNIT_REPORTER
#define TUT_CPPUNIT_REPORTER

#include <tut/tut.hpp>
#include <string>
#include <fstream>
#include <vector>
#include <stdexcept>

namespace tut
{

/**
 * CppUnit TUT reporter
 */
class cppunit_reporter : public tut::callback
{
    private:
        std::vector<tut::test_result> failed_tests_;
        std::vector<tut::test_result> passed_tests_;
        std::string filename_;

        std::string encode(const std::string & text)
        {
            std::string out;

            for (unsigned int i=0; i<text.length(); ++i) {
                char c = text[i];
                switch (c) {
                    case '<':
                        out += "&lt;";
                        break;
                    case '>':
                        out += "&gt;";
                        break;
                    case '&':
                        out += "&amp;";
                        break;
                    case '\'':
                        out += "&apos;";
                        break;
                    case '"':
                        out += "&quot;";
                        break;
                    default:
                        out += c;
                }
            }

            return out;
        }

public:

    cppunit_reporter(const std::string & filename = "testResult.xml")
        : failed_tests_(),
          passed_tests_(),
          filename_(filename)
    {
    }

    void run_started()
    {
        failed_tests_.clear();
        passed_tests_.clear();
    }

    void test_completed(const tut::test_result& tr)
    {
        if ( (tr.result == test_result::ok) ||
             (tr.result == test_result::skipped) )
        {
            passed_tests_.push_back(tr);
        }
        else
        {
            failed_tests_.push_back(tr);
        }
    }

    void run_completed()
    {
        int errors = 0;
        int failures = 0;
        std::string failure_type;
        std::string failure_msg;
        std::ofstream xmlfile;

        xmlfile.open(filename_.c_str(), std::ios::in | std::ios::trunc);
        if (!xmlfile.is_open()) {
            throw (std::runtime_error("Cannot open file for output"));
        }

        /* *********************** header ***************************** */
        xmlfile << "<?xml version=\"1.0\" encoding='ISO-8859-1' standalone='yes' ?>" << std::endl
                << "<TestRun>" << std::endl;

        /* *********************** failed tests ***************************** */
        if (failed_tests_.size() > 0) {
            xmlfile << "  <FailedTests>" << std::endl;

            for (unsigned int i=0; i<failed_tests_.size(); i++) {
                switch (failed_tests_[i].result) {
                    case test_result::fail:
                        failure_type = "Assertion";
                        failure_msg  = "";
                        failures++;
                        break;
                    case test_result::ex:
                        failure_type = "Assertion";
                        failure_msg  = "Thrown exception: " + failed_tests_[i].exception_typeid + '\n';
                        failures++;
                        break;
                    case test_result::warn:
                        failure_type = "Assertion";
                        failure_msg  = "Destructor failed.\n";
                        failures++;
                        break;
                    case test_result::term:
                        failure_type = "Error";
                        failure_msg  = "Test application terminated abnormally.\n";
                        errors++;
                        break;
                    case test_result::ex_ctor:
                        failure_type = "Error";
                        failure_msg  = "Constructor has thrown an exception: " + failed_tests_[i].exception_typeid + '\n';
                        errors++;
                        break;
                    case test_result::rethrown:
                        failure_type = "Assertion";
                        failure_msg  = "Child failed";
                        failures++;
                        break;
                    default:
                        failure_type = "Error";
                        failure_msg  = "Unknown test status, this should have never happened. "
                                       "You may just have found a BUG in TUT CppUnit reporter, please report it immediately.\n";
                        errors++;
                        break;
                }

                xmlfile << "    <FailedTest id=\"" << failed_tests_[i].test << "\">" << std::endl
                        << "      <Name>" << encode(failed_tests_[i].group) + "::" + encode(failed_tests_[i].name) << "</Name>" << std::endl
                        << "      <FailureType>" << failure_type << "</FailureType>" << std::endl
                        << "      <Location>" << std::endl
                        << "        <File>Unknown</File>" << std::endl
                        << "        <Line>Unknown</Line>" << std::endl
                        << "      </Location>" << std::endl
                        << "      <Message>" << encode(failure_msg + failed_tests_[i].message) << "</Message>" << std::endl
                        << "    </FailedTest>" << std::endl;
            }

            xmlfile << "  </FailedTests>" << std::endl;
        }

        /* *********************** passed tests ***************************** */
        if (passed_tests_.size() > 0) {
            xmlfile << "  <SuccessfulTests>" << std::endl;

            for (unsigned int i=0; i<passed_tests_.size(); i++) {
                xmlfile << "    <Test id=\"" << passed_tests_[i].test << "\">" << std::endl
                        << "      <Name>" << encode(passed_tests_[i].group) + "::" + encode(passed_tests_[i].name) << "</Name>" << std::endl
                        << "    </Test>" << std::endl;
            }

            xmlfile << "  </SuccessfulTests>" << std::endl;
        }

        /* *********************** statistics ***************************** */
        xmlfile << "  <Statistics>" << std::endl
                << "    <Tests>" << (failed_tests_.size() + passed_tests_.size()) << "</Tests>" << std::endl
                << "    <FailuresTotal>" << failed_tests_.size() << "</FailuresTotal>" << std::endl
                << "    <Errors>" << errors << "</Errors>" << std::endl
                << "    <Failures>" << failures << "</Failures>" << std::endl
                << "  </Statistics>" << std::endl;

        /* *********************** footer ***************************** */
        xmlfile << "</TestRun>" << std::endl;

        xmlfile.close();
    }

    virtual bool all_ok() const
    {
        return failed_tests_.empty();
    };


};

}

#endif


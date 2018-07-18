#include <tut/tut.hpp>

#include <limits>

namespace tut
{
	/**
	* Testing ensure() method.
	*/
	struct ensure_isnan_isinf_test
	{
		virtual ~ensure_isnan_isinf_test()
		{
		}
	};

	typedef test_group<ensure_isnan_isinf_test> tf;
	typedef tf::object object;
	tf ensure_isnan_isinf_test("ensure_isnan_isinf");

	/**
	* Checks ensure_isnan
	*/
	template<>
	template<>
	void object::test<1>()
	{
		set_test_name("checks ensure_isnan");

		double zero = 0.;
		ensure_isnan("ok", 0. / zero);
		ensure_isnan(std::numeric_limits<double>::quiet_NaN());
	}

	/**
	* Checks ensure_not_isnan
	*/
	template<>
	template<>
	void object::test<2>()
	{
		set_test_name("checks ensure_not_isnan");

		ensure_not_isnan("ok", 12.);
		ensure_not_isnan(std::numeric_limits<double>::infinity());
	}

	/**
	* Checks ensure_isinf
	*/
	template<>
	template<>
	void object::test<3>()
	{
		set_test_name("checks ensure_isinf");

		double zero = 0.;
		ensure_isinf("ok", 1. / zero);
		ensure_isinf("ok", -1. / zero);
		ensure_isinf(std::numeric_limits<double>::infinity());
	}

	/**
	* Checks ensure_isfinite
	*/
	template<>
	template<>
	void object::test<4>()
	{
		set_test_name("checks ensure_isfinite");

		ensure_isfinite("ok", 12.);
		ensure_isfinite(1000000);
	}
}

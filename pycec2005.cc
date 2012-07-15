#include <Python.h>
#include <boost/python.hpp>
#include <boost/python/numeric.hpp>
#include <boost/python/list.hpp>
#include <iostream>
#include "cec2005/cec2005.h"
#include "cec2005/srandom.h"

using namespace boost::python;

Random r(new SRandom(12345679));

void set_function(int fun, int dim) {
    init_cec2005(&r, fun, dim);
}

list get_domain(int fun) {
    list domain;
    char name[100];
    double min, max, optime;

    getInfo_cec2005(fun, name, &min, &max, &optime);
    domain.append(min);
    domain.append(max);
    return domain;
}

bool is_bound(void) {
   return isBound_cec2005();
}

double evalua(const numeric::array &el) {
   const tuple &shape = extract<tuple>(el.attr("shape")); 
   unsigned n = boost::python::extract<unsigned>(shape[0]);
   double *tmp = new double[n];
  for(unsigned int i = 0; i < n; i++)
    {
      tmp[i] = boost::python::extract<double>(el[i]);
    }
  double result = eval_cec2005(tmp, n);
  delete tmp;
  return result; 
}

double evalua_array(list el) {
   unsigned n = len(el);
   double *tmp = new double[n];
   for(unsigned i = 0; i < n; i++)
    {
      tmp[i] = extract<double>(el[i]);
    }
  double result = eval_cec2005(tmp, n);
  delete tmp;
  return result; 
}



BOOST_PYTHON_MODULE(libpycec2005)
{
    using namespace boost::python;
    numeric::array::set_module_and_type( "numpy", "ndarray");
    def("config", &set_function);
    def("domain", &get_domain);
    def("isBound", &is_bound);
    def("evaluate", &evalua);
    def("eval", &evalua_array);
}

/**
 * Copyright 2008, Daniel Molina Cabrera
 * 
 * This file is part of software Realea
 * 
 * Realea is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * Realea is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef _PROBLEM_CEC2005_H

#define _PROBLEM_CEC2005_H 1

#include "../common/problemfactory.h"

class ProblemCEC2005 : public ProblemFactory {
   public:
       ProblemCEC2005(unsigned int dim);
       ~ProblemCEC2005(void);
       ConfigProblem *get(unsigned int ident=1);
       /**
	* Enable the CEC2005 library
	*/
       void init(unsigned int fun); 

    private:
	unsigned int m_ndim;
	bool m_init;
};



#endif

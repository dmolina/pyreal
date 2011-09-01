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

#include "problemeasy.h"
#include "functions.h"

ProblemEasy::ProblemEasy(unsigned int dim)  {
   m_ndim = dim;
}

ProblemEasy::~ProblemEasy(void) {
}

ConfigProblem *ProblemEasy::get(unsigned int fun) {
    ConfigProblem* prob = new ConfigProblem();
    prob->setDimension(m_ndim);
    double min = -2.56;
    double max = 5.12;
    
    for (unsigned i = 0; i < m_ndim; ++i) {
	prob->setDomainValues(i, min, max, true);
    }

    // Defino el criterio de óptimo
    prob->setOptimize(minimize, 0);

    // Defino la función de fitness
    prob->setEval(sphere);

    return prob;
}

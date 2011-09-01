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

#include "problemcec2005.h"
#include "cec2005/cec2005.h"


ProblemCEC2005::ProblemCEC2005(Random *random, unsigned int dim) {
    m_random = random;
    m_ndim = dim;
    m_init = false;
}

ProblemCEC2005::~ProblemCEC2005(void) {
    if (m_init) {
	finish_cec2005();
    }
}


void ProblemCEC2005::init(unsigned int fun) {
     if (m_init) {
	finish_cec2005();
	m_init = false;
    }

    init_cec2005(m_random,nun, m_ndim);
    m_init = true;

   
}


ConfigProblem *ProblemCEC2005::get(unsigned int fun) {
    string name;
    double min, max, optime;

    // Limpio si se pidió alguna otra función anteriormente
    init(fun);
    getInfo_cec2005(fun, name, min, max, optime);

    ConfigProblem* prob = new ConfigProblem();
    prob->setDimension(m_ndim);
    
    for (unsigned i = 0; i < m_ndim; ++i) {
	prob->setDomainValues(i, min, max, true);
    }

    // Defino el criterio de óptimo
    prob->setOptimize(minimize, optime);
    prob->setUmbral(1e-8);

    // Defino la función de fitness
    prob->setEval(eval_cec2005);
    return prob;
}

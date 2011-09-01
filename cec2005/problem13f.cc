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

#include "problem13f.h"
#include "functions.h"

static FUNCTION normalFun[] = 
     {
	{1, 25, "sphere", sphere, {-2.56, 5.12}, {-2.56, 5.12}, 0},
	{2, 25, "schwefel_12", schwefel_12, {-35.0,95.0}, {-35.0,95.0}, 0},
        {3, 25, "rastrigin", rastrigin, {-8.5,1.5}, {-8.5,1.5}, 0},
        {4, 25, "griewank", griewank, {-200, 1000}, {-200, 1000}, 0}, 
        {5, 25, "ef10", ef10, {-80, 120}, {-80, 120}, 0},
        {6, 25, "rosenbrock", rosenbrock, {-5.12, 5.12}, {-5.12, 5.12}, 0},
      	{7, 10, "sle", sle, {-127,127}, {-127,127}, 0},
	{8, 6, "fms", fms, {-6.4, 6.35}, {-6.4, 6.35}, 0},
	{9, 9, "cheb9", cheb9, {-512, 512}, {-512, 512}, 0},
	{10, 25, "ackley", ackley, {-15.0, 30.0}, {-15.0, 30.0}, 0},
	{11, 2, "bohachevsky", bohachevsky, {-5.5, 6.5}, {-5.5, 6.5}, 0},
	{12, 6, "watson", watson, {-2,2}, {-2,2}, 2.288},
	{13, 25, "colville", colville, {-10.0, 10.0}, {-10.0, 10.0}, 0}, 
     };

Problem13F::Problem13F(void) : ProblemTableFactory(normalFun, 13) {
}

Problem13F::~Problem13F(void) {}

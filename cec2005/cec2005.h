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

#ifndef _CEC2005_H 

#define _CEC2005_H 1

#include <stdio.h>
#include <stdlib.h>

#include <string>
#include "global.h"
#include "rand.h"
#include "sub.h"
#include "define.h"

using namespace std;

#ifndef _tGen
typedef long double tGen;
#define _tGen
#endif

/**
 * Este m�todo permite indicar si debe de comprobar los l�mites
 * 
 * @return booleano que indsica si se debe de comprobar o no
 */
bool isBound_cec2005(void);

/**
 * Este m�todo permite iniciar el modo de funcionamiento de las funciones del CEC2005
 *
 * @param random generador de n�meros aleatorios
 * @param nfun funci�n a evaluar
 * @param dim dimensi�n
 */
void init_cec2005(Random *random, int nfun, int dim);

/**
 * Funci�n de evaluaci�n 
 *
 * @param x soluci�n a evaluar (iniciada en la posici�n 0)
 * @param ndim Longitud de la dimensi�n (se ignora)
 */
double eval_cec2005(const long double *x, int ndim);
double eval_cec2005(const double *x, int ndim);


/**
 * Permite liberar recursos cuando ya no se vaa a realizar m�s evaluaciones
 *
 */
void finish_cec2005(void); 

/**
 * ste m�todo permite obtener informaci�n sobre la funci�n
 * @param fun identificador de la funci�n
 * @param name Nombre de la funci�n.
 * @param min valor m�nimo del rango
 * @param max valor m�ximo del rango
 * @param optime valor optimo a comprobar
 */
void getInfo_cec2005(int fun, char *name, double *min, double *max, double *optime);

#endif

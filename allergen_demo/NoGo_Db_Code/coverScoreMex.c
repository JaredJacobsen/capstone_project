#include "mex.h"
#include "math.h"

/*
 * xtimesy.c - example found in API guide
 *
 * multiplies an input scalar times an input matrix and outputs a
 * matrix
 *
 * This is a MEX-file for MATLAB.
 * Copyright 1984-2006 The MathWorks, Inc.
 */

/* $Revision: 1.10.6.2 $ */

void xtimesy(double *y, double *z, mwSize m, mwSize n, double *x, mwSize mX, mwSize nX) {
	mwSize i, j, k, firstStart, secondStart;
	double coVar;
	
	for (i=0; i< n ; i++) {

		firstStart = i*m;	
		
		for (j= 0; j < nX; j++) {
			
			/*Calculate the corr*/

			coVar = 0;
			secondStart = j*mX;
			

			for (k=0; k < mX; k++) {
				coVar += fmin(*(x+ (secondStart + k)), *(y+ (firstStart + k)));
			}

			if (coVar > *(z+i))
				*(z+i) = coVar;

		}
	}
}

/* the gateway function */
void mexFunction( int nlhs, mxArray *plhs[],
		int nrhs, const mxArray *prhs[]) {
	double *y, *z, *x;
	mwSize mrows, ncols, mrowsX, ncolsX;
	int i = 0;
	
	/*  check for proper number of arguments */
	/* NOTE: You do not need an else statement when using mexErrMsgTxt
	 * within an if statement, because it will never get to the else
	 * statement if mexErrMsgTxt is executed. (mexErrMsgTxt breaks you out of
	 * the MEX-file) */
	if(nrhs!=2)
		mexErrMsgTxt("Two inputs required.");
	if(nlhs!=1)
		mexErrMsgTxt("One output required.");
	
	/* check to make sure the first input argument isn't complex */
	if(  mxIsComplex(prhs[0])) {
		mexErrMsgTxt("Input x must be real.");
	}
	
	
	/*  create a pointer to the input matrix y */
	y = mxGetPr(prhs[0]);
	x = mxGetPr(prhs[1]);
	
	/*  get the dimensions of the matrix input y */
	mrows = mxGetM(prhs[0]);
	ncols = mxGetN(prhs[0]);
	
	mrowsX = mxGetM(prhs[1]);
	ncolsX = mxGetN(prhs[1]);
	
	if(mrowsX!=mrows)
		mexErrMsgTxt("Row Lengths don't match");
	
	
	/*
	 * print("%i", rowlength);
	 */
	/*  set the output pointer to the output matrix */
	plhs[0] = mxCreateDoubleMatrix(ncols, 1, mxREAL);
	
	/*  create a C pointer to a copy of the output matrix */
	z = mxGetPr(plhs[0]);
	
	for (i=0; i< ncols ; i++) {
		*(z+i) = -1;
	}
	
	/*  call the C subroutine */
	xtimesy(y, z, mrows, ncols, x, mrowsX, ncolsX);
	
}

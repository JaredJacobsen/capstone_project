NoGo Negative Example Calculation Code
© Noah Youngs, 2014, All Rights Reserved

This code contains implementations of the SNOB, NETL and Rocchio algorithms for negative example prediction in protein function prediction (predicting which proteins do NOT perform which GO functions).

Input data must be formatted correctly. For an example of such data from Yeast, see the included file 'yeast.mat'. For a description of the data structure, see the comments at the beginning of 'negativeExampleGenerator.m'.

The SNOB and Rocchio algorithms are self-contained, but the NETL algorithm requires an LDA package, specifically the one written by Daichi Mochihashi which is available at http://chasen.org/~daiti-m/dist/lda/. In addition, you will have to train the LDA topic model for your specific data. This can be done with the same package, or with the C-version of LDA available from Blei. The output files should be *.alpha and *.beta, where *.alpha is a nx1 vector where n is the number of chosen topics, and *.beta is an m x n matrix where m is the number of GO-terms with annotations in your data (the "words") and n is the number of topics. We recommend choosing n to be the number of direct children with annotations in your data of the 3 roots of the go tree (this number changes as GO is updated, and depending on the completeness of annotation of a particular organism, but usually ranges between 35-60). LDA code should be placed in the 'ldaPosterierCode' folder. In addition, you may need to recompile coverScoreMex.c for your architecture if you are not using an intel mac. If so, use the standard "mex" command from within matlab.

For an overview of these algorithms, see the publication: Youngs, N, et al. "Negative Example Selection For Protein Function Prediction: The NoGO database". Available at:
http://bonneaulab.bio.nyu.edu/noGo
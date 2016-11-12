function [goProb] = coProbCalc(goTermEvidence, column, params)
% CoProbCalc Compute the empirical probability of Go term i appearing given
% go term j has appeared
%   goProb = coProbCalc(goTermEvidence, column, params) returns an r x r 
%   matrix containing in its (i,j)th entry the empirical probability that
%   empirical probability that go term i will be present given that go term
%   j is present, where r= length(column). goTermEvidence must be an n x m 
%   binary matrix with n being the number of genes, m the number of go 
%   categories, and a 1 in the (i,j)th entry if gene i has go term j. 
%   Column is an n x 1 vector of column indicies to calculte the empirical 
%   probabilities for. Params is a struct containing the pseudocounting
%   parameters, with params[1] = lambda and params[2] = gamma.
%
%   goProb = coProbCalc(goTermEvidence, params) returns an m x m matrix, 
%   identical to the one above but for all columns in goTermEvidence.

if (nargin  == 3 )
    goProb = goTermEvidence'*(goTermEvidence(:,column));    %calculate the times both terms appear together
elseif (nargin == 2)
    goProb = goTermEvidence'*goTermEvidence;            %calculate the times both terms appear together
    params =  column;
end

%Divide each column by the number of times annotation j appears, with
%pseudocounts added
for i = 1:size(goProb,1)
    goProb(i,:) = goProb(i,:) ./ (sum(goTermEvidence(:,i)) + params(1)*exp(params(2)*sum(goTermEvidence(:,i))));
end

end
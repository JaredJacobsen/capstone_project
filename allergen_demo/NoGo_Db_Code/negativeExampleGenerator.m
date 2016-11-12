% NoGo Negative Example Calculation Code
% © Noah Youngs, 2014, All Rights Reserved

clear
currFile = 'yeast.mat';
inData=load(currFile);

%%%%%%%%%%
% The input file should be a matlab '.mat' file, containing a variable
% called 'currentData'. currentData is a struct vector of length 3, where
% each entry is one of the 3 branches of GO, ordered: BP, MF, CC.
% Each of these three entries should have the following fields:
%   branch: this identifies which branch of GO is stored, and should be one
%       of: ('BP', 'MF', 'CC')
%   rowLabels: the gene names of each row of data (these should be the same
%       across all three data structures)
%   columnLabels: the GO term names for each column of data (these will be
%       different in each of the 3 structures for each branch)
%   dataIEA: The binary annotation matrix, where each row is a
%       gene/protein, and each column is a GO term. A 1 indicates that 
%       there exists an annotation for that GO term to that protein. These
%       annotations should include IEA evidence codes.
%   data: The same as the dataIEA structure, except now annotations with
%       IEA evidence codes should be excluded.
%   dataNOT: The binary annotation matrix of negative annotations in GO
%       (there are usually very few, if any, of these)
%   parents: A binary matrix of size m x m, where m is the number of GO
%       terms in this branch. There is a 1 in entry (i,j) if the ith GO
%       term is a direct parent of the jth GO term in the GO tree.
%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
algorithm = 'NETL';          % Algorithm Selector, choose between 'Rocchio', 'SNOB', and 'NETL'
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fprintf(1, 'Generating negative examples using the algorithm: %s\n', algorithm);
n = length(inData.currentData{1}.rowLabels);

% Rocchio algorithm initialization
if strcmp(algorithm,'Rocchio')
    
    % combine annotations from all 3 branches into one branch
    docMat = [inData.currentData{1}.dataIEA inData.currentData{2}.dataIEA inData.currentData{3}.dataIEA];
    
    %find genes that have at least one annotation
    usableInds = find(sum(docMat));
    
    %compute the idf vector
    idfVec = log(n ./  sum(docMat(:,usableInds)));
    
    %compute the d matrix, piecewise to avoid memory issues
    dMat = docMat;
    for i = 1:10
        chunk = round(n / 10);
        blockEnd = min(n, (i*chunk));
        blockBegin = (i-1)*chunk + 1;
        dMat(blockBegin:blockEnd,:) = docMat(blockBegin:blockEnd,usableInds).*repmat(idfVec,blockEnd-blockBegin +1,1);
    end
    
    %normalize the d matrix, set alpha and beta to standard values
    normSet = sqrt(sum(abs(dMat).^2,2));
    dMatNorm = diag(normSet.^-1) *  dMat;
    alp = 16;
    bet = 4;
    
    % find the indices of the root GO terms (the terms with the most
    % annotations, assuming all GO terms were pulled) and keep track of
    % which genes only have root annotations and nothing more specific.
    % These should not be considered in any calculations
    multVec = zeros(size(docMat,2),1);
    rootLocs = [ 0 0 0 ];
    for i = 1:3
        colSums = sum(inData.currentData{i}.data);
        rootLocs(i) = find(colSums == max(colSums));
        
    end
    multVec(rootLocs(1))= 1;
    multVec(size(inData.currentData{1}.dataIEA,2) + rootLocs(2)) = 1;
    multVec(size(inData.currentData{1}.dataIEA,2) + size(inData.currentData{2}.dataIEA,2) + rootLocs(3)) = 1;
    
    hasThree = docMat*multVec;
    allAnnots = sum(docMat,2);
    
    noGo = find(hasThree == allAnnots);
end

% SNOB algorithm initialization
if strcmp(algorithm, 'SNOB')
    combo = [inData.currentData{1}.dataIEA inData.currentData{2}.dataIEA inData.currentData{3}.dataIEA];
    
    % clear out the annotations for the root GO terms
    for i = 1:3
        colSums = sum(inData.currentData{i}.data);
        combo(:,find(colSums == max(colSums))) = 0;   
    end
    
    % find the terms that have any annotations, and the weight vector
    anyGo = find(sum(combo'));
    wComb = diag(sum(combo').^-1);
    
    % try and load the co-probability file
    storeFile = ['coProbMat_' currFile '_Store.mat'];
    try 
        fprintf(1, 'Loading co-probability file\n');
        coprobFile = load(storeFile);
        coProbMatIEA = coprobFile.coProbMatIEA;
        clear coprobFile;
    catch e
        % the file didn't exist, so we recalculate. We don't want to use
        % pseudo-counts so pass in 0's for those params
        fprintf(1, 'Could not load file. Calculating Co-Probabilities (this may take up to an hour if the number of GO categories is large)\n');
        coProbMatIEA = coProbCalc(combo, [0 0]);
        save(storeFile, 'coProbMatIEA');
    end    
end

% NETL algorithm initialization
if strcmp(algorithm, 'NETL')
    
    fprintf(1, 'Adjusting format of data to make it LDA-compatible (this may take a couple minutes)\n');
    % turn the annotations into a word-count style document data structure
    [docMat, dex2mat] = mat2count([inData.currentData{1}.dataIEA inData.currentData{2}.dataIEA inData.currentData{3}.dataIEA ]);
    usable = find(dex2mat > 0);
    
    fprintf(1, 'Loading trained model\n');
    % load the LDA model params (These need to be computed with an external
    % package. See the ReadMe for details).
    alpha20 = load(['model_' currFile '.alpha']);
    beta20 = load(['model_' currFile '.beta']);

    fprintf(1, 'Computing the posterior topic liklihood for all proteins\n');
    addpath('./ldaPosteriorCode')
    topsHere = zeros(n,length(alpha20));
    for g = find(dex2mat > 0)' 
        post = vbem(docMat{dex2mat(g)},beta20,alpha20);
        topsHere(g,:) = post./sum(post);
    end  
end


geneNamesForPrinting = inData.currentData{1}.rowLabels;
geneNamesForPrinting{length(geneNamesForPrinting) + 1} = 'NONE';

% iterate through the three branches of GO, calculating negative example
% rankings for each GO term
for branchDex = 1:3
    fprintf(1, '%s\n', inData.currentData{branchDex}.branch)
    
    %print out negative examples per branch
    foo = fopen([algorithm '_' currFile '_' inData.currentData{branchDex}.branch '.txt'], 'w');
    
    % make sure branches are in the order we expect
    if branchDex == 1 && (~strcmp(inData.currentData{branchDex}.branch,'BP') || ~strcmp(inData.validationData{branchDex}.branch,'BP'))
        error('Expected branch to be biological process')
    elseif branchDex == 2 && (~strcmp(inData.currentData{branchDex}.branch,'MF') || ~strcmp(inData.validationData{branchDex}.branch, 'MF'))
        error('Expected branch to be molecular function')
    elseif branchDex == 3 && (~strcmp(inData.currentData{branchDex}.branch,'CC') || ~strcmp(inData.validationData{branchDex}.branch, 'CC'))
        error('Expected branch to be cellular component')
    end
    
    %get the number of GO terms
    m = length(inData.currentData{branchDex}.columnLabels);
    
    % calculate the offset that tells us where this particular branch of GO
    % starts within the matrix containing all 3 branches
    offSet = 0;
    for pastDex = 1:branchDex-1
        offSet = offSet + length(inData.currentData{pastDex}.columnLabels);
    end
    
    
    % predict negatives for each GO term
    for sampleCat = 1 : m
        if (mod(sampleCat,500) == 0)
            fprintf(1,'%2.0f%%\t', 100*sampleCat / m)
        end
        
        % get the existing annotations (non-IEA)
        annotPos = find(inData.currentData{branchDex}.data(:, sampleCat));
        
        if strcmp(algorithm, 'Rocchio')
            
            % divide the proteins into positive and non-positive (including
            % IEA annotations)
            posInds = find(inData.currentData{branchDex}.dataIEA(:,sampleCat));
            numPos = length(posInds);
            restInds = setdiff(1:n, posInds);
            numRest = length(restInds);
            
            % calculate the minus and plus vectors
            cplus = alp / numPos * sum(dMatNorm(posInds,:)) - bet / numRest * sum(dMatNorm(restInds,:));
            cminus = alp / numRest* sum(dMatNorm(restInds,:)) - bet / numPos * sum(dMatNorm(posInds,:));
            
            cplusNorm = norm(cplus,2);
            cminusNorm = norm(cminus,2);
            
            
            plusScores = diag((cplusNorm*normSet).^-1)*dMat*cplus';
            minusScores = diag((cminusNorm*normSet).^-1)*dMat*cminus';
            
            cpn = cplus ./ cplusNorm;
            cmn = cminus ./ cminusNorm;
            
            % compute the scores for all proteins
            plusScores2 = dMatNorm*cpn';
            minusScores2 = dMatNorm*cmn';
            
            % create the difference vector, where a higher number means the
            % protein is closer to the neagtive class than the positive
            diffs = minusScores - plusScores;
            
            % make sure proteins that have positive annotations or that
            % don't have any go terms to use to call them a negative
            % example get ranked last.
            diffs(posInds) = -2;
            diffs(noGo) = -1.5;
            [val,dex] = sort(diffs,1,'descend');
            
        end
        
        if strcmp(algorithm, 'SNOB')
            
            % define the set of possible negatives, and existing positives
            negGenes = anyGo;
            posInds = find(inData.currentData{branchDex}.dataIEA(:,sampleCat));
            possible = setdiff(anyGo, posInds);
            
            % calculate the score from the existing annotations, the weight
            % vector, and the coProbability matrix
            thisPotentialProbs = ...
                wComb*combo*coProbMatIEA(:,sampleCat + offSet);
            
            negGenes = setdiff(negGenes,find(inData.currentData{branchDex}.dataIEA(:,sampleCat)));
            noGo = setdiff(1:n, negGenes);
            
            % make sure positively-labeled proteins and proteins with no go
            % terms end up last when sorting the score vector (lower scores
            % are more likely to be negative.
            thisPotentialProbs(noGo) = 1.5;
            thisPotentialProbs(posInds) = 2;
            [val, dex] = sort(thisPotentialProbs,1,'ascend');
            
        end
        
        if strcmp(algorithm, 'NETL')
            posInds = find(inData.currentData{branchDex}.dataIEA(:,sampleCat));
            scores = zeros(n,1);
            scores(usable) = 1 - coverScoreMex(topsHere(usable,:)', topsHere(posInds,:)');
            scores(posInds) = -2;
            noGo = setdiff(1:n, usable);
            scores(noGo) = -1;
            [val, dex] = sort(scores,'descend');
        end
        
        % print out the gene names in the order of most to least likely to
        % be a negative example for the given GO category. Make the last
        % set of proteins which are positive for this gene or which have no
        % GO terms show up in the file as "NONE".
        dex(end-(length(union(posInds,noGo)) - 1):end) = length(geneNamesForPrinting);
        fprintf(foo, '%s\t', inData.currentData{branchDex}.columnLabels{sampleCat});
        fprintf(foo,'%s\t', geneNamesForPrinting{dex});
        fprintf(foo, '\n');       
    end
    fprintf(1,'done\n')
    fclose(foo);
end

fprintf(1, '\n\nNegative example calculation complete\n\n')


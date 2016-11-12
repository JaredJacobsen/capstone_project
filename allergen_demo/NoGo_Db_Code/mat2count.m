function [ doc, dex2mat ] = mat2count( data )
% turn a binary matrix into a count if entries, along with the location of
% the index in the matrix

doc = {};
docCount = 0;
dex2mat = zeros(size(data,1),1);
for i = 1:size(data,1)
    annots = find(data(i,:));
    if ~isempty(annots)
        docCount = docCount + 1;
        doc{docCount}.id = annots;
        doc{docCount}.cnt = data(i,annots);
        doc{docCount}.fullDex = i;
        dex2mat(i) = docCount;
    end
end

end


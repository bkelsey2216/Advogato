% Brooke Kelsey & Natalie Pollard
% this script computes the expected belief and entropy of each node in group X.
% upon completion of this script, the appropriate columns from the four output matricies 
% (pubBeliefX, pubEntropyX, trustorBeliefX, trustorEntropyX) can be loaded into the CDF 
% distribution fit to produce overlaying CDFs with the corresponding group Y data.
%
% Assumes input .csv file is named testCSVX

%expected belief using public opinion 
for x = 1:length(testCSVX) 
    pubOpnVectorX(x, (1:4)) = [testCSVX(x,9) testCSVX(x,10) testCSVX(x,11) testCSVX(x,12)];
    pubBeliefX(x,2) = [expbelief(pubOpnVectorX(x,(1:4)))];
    pubBeliefX(x,1) = [testCSVX(x,2)];
end

%expected belief using individual final opinions
for x = 1:length(testCSVX)
    trustorOpnVectorX(x, (1:4)) = [testCSVX(x,5) testCSVX(x,6) testCSVX(x,7) testCSVX(x,8)];
    trustorBeliefX(x,2) = [expbelief(trustorOpnVectorX(x,(1:4)))];
    trustorBeliefX(x,1) = [testCSVX(x,2)];
end

%entropy of public opinions
for x = 1:length(pubOpnVectorX)
    
    %extract evidences from opinion vector
    b = pubOpnVectorX(x,1);
    d = pubOpnVectorX(x,2);
    n = pubOpnVectorX(x,3);
    e = pubOpnVectorX(x,4);
    
    r = b*(3/e)+1+1;
    s = d*(3/e)+1+1;
    
    %compute entropy
    ent = log(beta(r,s))-((r-1).*psi(r))-((s-1).*psi(s))+((r+s-2).*psi(r+s));
    
    %if result is -Inf, replace with -20 so that CDF will process data
    if ent == -Inf
        entropyCellsX(x,2) = {-20};
    else
        entropyCellsX(x, 2) = {ent};
    end
   
    %add node ID as first column
    entropyCellsX(x, 1) = {testCSVX(x, 2)};
end

% convert the cell array to a matrix
pubEntropyX = cell2mat(entropyCellsX);

%entropy of trustor opinions
for x = 1:length(trustorOpnVectorX)
    b = trustorOpnVectorX(x,1);
    d = trustorOpnVectorX(x,2);
    n = trustorOpnVectorX(x,3);
    e = trustorOpnVectorX(x,4);

    r = b*(3/e)+1+1;
    s = d*(3/e)+1+1;
    
    ent = log(beta(r,s))-((r-1).*psi(r))-((s-1).*psi(s)) + ((r+s-2).*psi(r+s));
    
    if ent == -Inf
        entropyCellsX(x,2) = {-20};
    else
        entropyCellsX(x, 2) = {ent};
    end
    
    entropyCellsX(x, 1) = {testCSVX(x, 2)};
end

trustorEntropyX = cell2mat(entropyCellsX);
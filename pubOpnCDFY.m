% Brooke Kelsey & Natalie Pollard
% this script computes the expected belief and entropy of each node in group Y.
% upon completion of this script, the appropriate columns from the four output matricies 
% (pubBeliefY, pubEntropyY, trustorBeliefY, trustorEntropyY) can be loaded into the CDF 
% distribution fit to produce overlaying CDFs with the corresponding group X data.
%
% Assumes input .csv file is named testCSVY

%expected belief using public opinion
for x = 1:length(testCSVY) 
    pubOpnVectorY(x, (1:4)) = [testCSVY(x,9) testCSVY(x,10) testCSVY(x,11) testCSVY(x,12)];
    pubBeliefY(x,2) = [expbelief(pubOpnVectorY(x,(1:4)))];
    pubBeliefY(x,1) = [testCSVY(x,2)];
end


%expected belief using individual final opinions
for x = 1:length(testCSVY)
    trustorOpnVectorY(x, (1:4)) = [testCSVY(x,5) testCSVY(x,6) testCSVY(x,7) testCSVY(x,8)];
    trustorBeliefY(x,2) = [expbelief(trustorOpnVectorY(x,(1:4)))];
    trustorBeliefY(x,1) = [testCSVY(x,2)];
end

%entropy of public opinions
for x = 1:length(pubOpnVectorY)
    
    %extract evidences from opinion vector
    b = pubOpnVectorY(x,1);
    d = pubOpnVectorY(x,2);
    n = pubOpnVectorY(x,3);
    e = pubOpnVectorY(x,4);
    
    r = b*(3/e)+1+1;
    s = d*(3/e)+1+1;
    
    %compute entropy
    ent = log(beta(r,s))-((r-1).*psi(r))-((s-1).*psi(s))+((r+s-2).*psi(r+s));
    
    %if result is -Inf, replace with -20 so that CDF will process data
    if ent == -Inf
        entropyCellsY(x,2) = {-20};
    else
        entropyCellsY(x, 2) = {ent};
    end
   
    %add node ID as first column
    entropyCellsY(x, 1) = {testCSVY(x, 2)};
end

% convert the cell array to a matrix
pubEntropyY = cell2mat(entropyCellsY);

%entropy of trustor opinions
for x = 1:length(trustorOpnVectorY)
    b = trustorOpnVectorY(x,1);
    d = trustorOpnVectorY(x,2);
    n = trustorOpnVectorY(x,3);
    e = trustorOpnVectorY(x,4);

    r = b*(3/e)+1+1;
    s = d*(3/e)+1+1;
    
    ent = log(beta(r,s))-((r-1).*psi(r))-((s-1).*psi(s)) + ((r+s-2).*psi(r+s));
    
    if ent == -Inf
        entropyCellsY(x,2) = {-20};
    else
        entropyCellsY(x, 2) = {ent};
    end
    
    entropyCellsY(x, 1) = {testCSVY(x, 2)};
end

trustorEntropyY = cell2mat(entropyCellsY);
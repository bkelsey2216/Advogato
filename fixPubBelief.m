% This script takes the output of pubOpnCDFX and pubOpnCDFY and creates a vector
% with no repeating nodeID-PublicOpinion entries. The output of this script produces 
% two cleaned up public opinion vectors (one for group X, one for Y) that can be loaded
% into the CDF distribution generator.

fixedPubBeliefX(1, (1:2)) = pubBeliefX(1, (1:2));
x = 2;
for i = 2:length(pubBeliefX)
    if pubBeliefX(i, 1) ~= pubBeliefX((i-1),1)
        fixedPubBeliefX(x, (1:2)) = pubBeliefX(i,(1:2));
        x = x+1;
    end
end


fixedPubBeliefY(1, (1:2)) = pubBeliefY(1, (1:2));
x = 2;
for i = 2:length(pubBeliefY)
    if pubBeliefY(i, 1) ~= pubBeliefY((i-1),1)
        fixedPubBeliefY(x, (1:2)) = pubBeliefY(i,(1:2));
        x = x+1;
    end
end

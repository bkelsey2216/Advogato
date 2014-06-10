% This code generates three bar graphs using the following imported
% dataset names:
%	VarName1 : Shortened version of one-hop dataset 
%	VarName2 : Shortened version of two-hop dataset
%	VarName3 : Shortened version of three-hop dataset
%
% Also, this code computes average reach (in proportion to the full
% set of nodes within the Advogato community) for each distribution,
% reported as a percentage. The following imported datasets 
% are referred to as:
%	VarName4 : Full one-hop dataset
%	VarName5 : Full two-hop dataset
%	VarName6 : Full three-hop dataset

%% create distribution 1

figure(1)
bar(VarName1)
title('One-Hop Distribution')
xlabel('Number of Nodes Reached with One Hop')
ylabel('Number of Nodes Capable of this Range')


%% create distribution 2

figure(2)
bar(VarName2)
title('Two-Hop Distribution')
xlabel('Number of Nodes Reached with Two Hops')
ylabel('Number of Nodes Capable of this Range')


%% create distribution 3

figure(3)
bar(VarName3)
title('Three-Hop Distribution')
xlabel('Number of Nodes Reached with Three Hops')
ylabel('Number of Nodes Capable of this Range')

dist1Sum = sum(VarName4);
dist2Sum = sum(VarName5);
dist3Sum = sum(VarName6);

reachDist1 = dist1Sum/6539
reachDist2 = dist2Sum/6539
reachDist3 = dist3Sum/6539
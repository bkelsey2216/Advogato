function result = expbelief(OpVect1)

%get the quantity of each component

b = OpVect1(1);
d = OpVect1(2);
n = OpVect1(3);
e = OpVect1(4);

%calculate the positive & negative evidence number. In the new definition 
%of expected belief, only positive and negative evidences will be accounted 
%Notice that besides priori and post evidence, an additional evidence is added for positive and
%negative evidences such that the post evidences will never be discounted
%to less then 1. 

r = b*(3/e)+1+1;
s = d*(3/e)+1+1;

%calculate the certainty
z = @(x) 0.5.*abs((betapdf(x,r,s) - 1));

cer = min((integral(z,0,1)),1);

result = ((b+(1/3)*e)*cer + 0.5*((b + d) + (2/3)*e)*(1 - cer))/(b+d+(2/3)*e);

end


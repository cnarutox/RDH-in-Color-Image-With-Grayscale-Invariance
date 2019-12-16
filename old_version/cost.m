function D=cost(V)
%   v1=abs(V(1)-V(3));
%   v2=abs(V(2)-V(3));
%   v3=abs(V(4)-V(3));
%   v4=abs(V(5)-V(3));
%   D=var([v1,v2,v3,v4]);
D=var(V);
end
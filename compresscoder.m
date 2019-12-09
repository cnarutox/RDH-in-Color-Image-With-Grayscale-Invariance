function Comp_bitstream=compresscoder(signal)
L=length(signal);
signal=double(signal);
minS=min(signal);
maxS=max(signal);
HistS=hist(signal,minS:maxS);
width=maxS-minS+1;
Ps=HistS/sum(HistS);
Freq=ones(L,width);
    for i=1:width
         Freq(:,i)=Ps(i)*Freq(:,i);
    end
signal=signal-min(signal)+1;
signal=reshape(signal,L,1);
bitstream=length(arith_encode(signal,Freq));



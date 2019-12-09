function [M_PER,M_PEG,M_PEB]=embed(PER,PEG,PEB,Mess,OBJ_ori,OBJ_emb,T)
L=length(Mess);
M_PER=PER;
M_PEG=PEG;
M_PEB=PEB;
    for i=1:L
%         M_PER=PER;
%         M_PEG=PEG;
%         M_PEB=PEB;
          [M_PER(i),M_PEG(i),M_PEB(i)]=embedonebit(PER(i),PEG(i),PEB(i),Mess(i),OBJ_ori,OBJ_emb,T);
    end

end
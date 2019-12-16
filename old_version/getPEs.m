function [PER, PEB, v_gray, pred_R, pred_B, cost_RB] = getPEs(Gray, img)
    warning off;
    % % addpath images\;
    % img=imread('lena.png');
    R = double(img(:, :, 1));
    B = double(img(:, :, 3));
    % % G=double(img(:,:,2));
    [ht, wd] = size(Gray);
    temp_dif_R = zeros(1, round(ht * wd / 2));
    temp_dif_B = zeros(1, round(ht * wd / 2));
    % temp_dif_R1=zeros(1,round(ht*wd/2));
    % temp_dif_B1=zeros(1,round(ht*wd/2));

    temp_pred_R = zeros(1, round(ht * wd / 2));
    temp_pred_B = zeros(1, round(ht * wd / 2));
    temp_cost_RB = zeros(1, round(ht * wd / 2));
    temp_gray = zeros(1, round(ht * wd / 2));
    %%%dir=0;%%%%%%%Ȧ��Ԥ��
    id = 0;

    for i = 2:ht - 1

        for j = 2:wd - 1

            id = id + 1;
            XR = [R(i + 1, j), R(i, j + 1), R(i + 1, j + 1)]; %,R(i+2,j),R(i,j+2)];
            %            XG=[G(i+1,j),G(i,j+1),G(i+1,j+1)];
            XB = [B(i + 1, j), B(i, j + 1), B(i + 1, j + 1)]; %,B(i+2,j),B(i,j+2)];
            XGray = [Gray(i + 1, j), Gray(i, j + 1), Gray(i + 1, j + 1)]; %,Gray(i+2,j),Gray(i,j+2)];
            temp_pred_R(id) = LSpredictor(XGray, XR, Gray(i, j));
            temp_pred_B(id) = LSpredictor(XGray, XB, Gray(i, j));
            temp_dif_R(id) = R(i, j) - temp_pred_R(id); %%%  abs<=1 0.4745
            temp_dif_B(id) = B(i, j) - temp_pred_B(id);
            temp_cost_RB(id) = cost([Gray(i - 1, j) Gray(i, j - 1) Gray(i, j) Gray(i + 1, j) Gray(i, j + 1)]); %%%abs<=1   0.4821 ���ѡ�� abs<=2  0.8144
            temp_gray(id) = Gray(i, j);
            %                  d_RB(id)=abs(Gray(i,j)-floor(sum([Gray(i-1,j)  Gray(i,j-1) Gray(i+1,j) Gray(i,j+1)])/4)); %%%abs<=1   0.4209
            %                  temp_dif_R(id)=R(i,j)-temp_dif_R(id);
            %                 temp_dif_Gray(id)=Gray(i,j)-MED(XGray);
            %                 temp_dif_R1(id)=R(i,j)-MED(XR);
            %                 temp_dif_B1(id)=B(i,j)-MED(XB);
            %
            %                  temp_dif_B(id)=B(i,j)-LSpredictor(XGray,XB,Gray(i,j));
            %                 temp_dif_B(id)=B(i,j)-temp_dif_B(id);
        end

    end

    PER = temp_dif_R(1:id);
    PEB = temp_dif_B(1:id);
    pred_R = temp_pred_R(1:id);
    pred_B = temp_pred_B(1:id);
    cost_RB = temp_cost_RB(1:id);
    v_gray = temp_gray(1:id);

    % PER1=temp_dif_R1(1:id);
    % PEB1=temp_dif_B1(1:id);
    % save PER_airplane PER
    % save PEB_airplane PEB
    %
    % save PER1_airplane PER1
    % save PEB1_airplane PEB1
    % % %
    % length(find(PER==0))
    % length(find(PEB==0))
    % %
    % length(find(PER1==0))
    % length(find(PEB1==0))
    % [~,id]=sort(cost_RB);
    % idx=id(1:10000);
    % as1=PER(idx);
    % as2=PEB(idx);
    % length( find(abs(as1)<=3))/length(as1)
    % length( find(abs(as2)<=3))/length(as2)
end

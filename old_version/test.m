filename = 'lena.png';
cover = double(imread(filename));
cR = 0.299;
cG = 0.587;
cB = 0.114;
gray = round(cR * cover(:, :, 1) + cG * cover(:, :, 2) + cB * cover(:, :, 3));
[PER, PEB, ~, pred_R, pred_B, cost] = getPEs(gray, cover);
messL0 = 10000:20000:130000;
messL = messL0;
psnr = zeros(length(messL), 1);
D = psnr;
N = psnr;

for i = 1:length(messL)
    tag = 1;
    D_T = 20;

    while tag
        [messL(i), psnr(i), T(i), N(i)] = main(round(1.02 * messL0(i)), D_T, gray, cover, PER, PEB, pred_R, pred_B, cost);

        if messL(i) >= messL0(i)
            tag = 0;
            D(i) = D_T;
            D_T
        else
            D_T = D_T + 5;
        end

    end

end

save messL_lena messL
save psnr_lena psnr
save D_lena D
save T_lena T
save N_lena N

%
% filename='airplane.png';
% cover=double(imread(filename));
% cR=0.299;
% cG=0.587;
% cB=0.114;
% gray=round( cR*cover(:,:,1)+cG*cover(:,:,2)+cB*cover(:,:,3) );
% [PER,PEB,~,pred_R,pred_B,cost]=getPEs(gray,cover);
% messL0=10000:20000:130000;
% messL=messL0;
% psnr=zeros(length(messL),1);
% D=psnr;
% N=psnr;
% for i=1:length(messL)
%     tag=1;
%     D_T=20;
%     while tag
%         [messL(i),psnr(i),T(i),N(i)]=main(round(1.02*messL0(i)),D_T,gray,cover,PER,PEB,pred_R,pred_B,cost);
%         if messL(i)>=messL0(i)
%             tag=0;
%             D(i)=D_T;
%             D_T
%
%         else
%             D_T=D_T+5;
%         end
%     end
% end
% save messL_airplane messL
% save psnr_airplane psnr
% save D_airplane D
% save T_airplane T
% save N_airplane N
% %
%
% filename='barbara.png';
% cover=double(imread(filename));
% cR=0.299;
% cG=0.587;
% cB=0.114;
% gray=round( cR*cover(:,:,1)+cG*cover(:,:,2)+cB*cover(:,:,3) );
% [PER,PEB,~,pred_R,pred_B,cost]=getPEs(gray,cover);
% messL0=10000:20000:130000;
% messL=messL0;
% psnr=zeros(length(messL),1);
% D=psnr;
% N=psnr;
% for i=1:length(messL)
%     tag=1;
%     D_T=20;
%     while tag
%         [messL(i),psnr(i),T(i),N(i)]=main(round(1.02*messL0(i)),D_T,gray,cover,PER,PEB,pred_R,pred_B,cost);
%         if messL(i)>=messL0(i)
%             tag=0;
%             D(i)=D_T;
%             D_T
%
%         else
%             D_T=D_T+5;
%         end
%     end
% end
% save messL_barbara messL
% save psnr_barbara psnr
% save D_barbara D
% save T_barbara T
% save N_barbara N
%
% filename='baboon.png';
% cover=double(imread(filename));
% cR=0.299;
% cG=0.587;
% cB=0.114;
% gray=round( cR*cover(:,:,1)+cG*cover(:,:,2)+cB*cover(:,:,3) );
% [PER,PEB,~,pred_R,pred_B,cost]=getPEs(gray,cover);
% messL0=10000:20000:130000;
% messL=messL0;
% psnr=zeros(length(messL),1);
% D=psnr;
% N=psnr
% bpp=1.09;
% for i=1:length(messL)
%     tag=1;
%     D_T=50;
%     bpp=1.1;
%     while tag
%         [messL(i),psnr(i),T(i),N(i)]=main(round(bpp*messL0(i)),D_T,gray,cover,PER,PEB,pred_R,pred_B,cost);
%         if messL(i)>=messL0(i)
%             tag=0;
%             b(i)=bpp;
%             D(i)=D_T;
%             D_T
%             bpp
%         else
%             if D_T<50
%             D_T=D_T+5;
%             else
%               bpp=bpp+0.01;
%             end
%         end
%     end
% end
% save messL_baboon messL
% save psnr_baboon psnr
% save D_baboon D
% save T_baboon T
% save N_baboon N
% save b_baboon b

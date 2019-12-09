function psnr=appraise_PSNR(img1,img2 )
%APPRAISE Summary of this function goes here
%   Detailed explanation goes here
img1=double(img1);
img2=double(img2);
L=length(img1(:));
mse = sum((img1(:)-img2(:)).^2)/L;

psnr=10*log10(255*255/mse);



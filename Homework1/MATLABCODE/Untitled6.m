close all;
Im = imread('Im2.jpg');
Im2 = Im;
Im2(:,:,1) = Im2(:,:,1)+50;
Im2(:,:,2) = Im2(:,:,2)+30;
Im2(:,:,3) = Im2(:,:,3)-50;

figure; imshow(Im);
figure; imshow(Im2);
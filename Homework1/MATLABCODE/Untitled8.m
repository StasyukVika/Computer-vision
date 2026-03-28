close all;
Im = imread('Im2.jpg');
Im = double(Im);
Imgray = 1/3*Im(:,:,1)+1/3*Im(:,:,2)+1/3*Im(:,:,3);
Im = uint8(Im);
Imgray = uint8(Imgray);
figure; imshow(Im);
figure; imshow(Imgray);
Imgray2 = rgb2gray(Im);
figure; imshow(Imgray2);

max(max(max(abs(Imgray2 - Imgray))));
surf(Imgray2 - Imgray)
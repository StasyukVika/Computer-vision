close all;
Im = imread('Im2.jpg');
Im2 = Im + 50;
Im3 = Im - 50;

figure; imshow(Im);
figure; imshow(Im2);
figure; imshow(Im3);

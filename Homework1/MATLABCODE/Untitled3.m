close all;
FirstIm = imread('Im1.jpg');
SecondIm = FirstIm;
SecondIm(10:200, 50:300,1:3) = 255 - SecondIm(10:200, 50:300,1:3);
figure; imshow(FirstIm)
figure; imshow(SecondIm)

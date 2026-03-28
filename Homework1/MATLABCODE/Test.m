close all;
MyImage = imread('N1.png');
whos MyImage
size(MyImage)
Red = MyImage; Green = MyImage; Blue = MyImage;
Red(:,:,[2,3]) = 0;
Green(:,:,[1,3]) = 0;
Blue(:,:,[1,2]) = 0;

figure; 
subplot(3,2,1); imshow(MyImage);
subplot(3,2,2); imshow(Red);
subplot(3,2,3); imshow(Green);
subplot(3,2,4);  imshow(Blue);
Neg = 255-MyImage;
subplot(3,2,5);  imshow(Neg);

% з 100 до 150 по рядках і з 150 до 200 по стовпцях зробити негатив
Neg2 = MyImage;
Neg2(100:150,150:200,:) = 255-Neg2(100:150,150:200,:);
subplot(3,2,6);  imshow(Neg2);
close all;
MyImage = imread('N1.png');
MyImage = double(MyImage);
Gray = 1/3*MyImage(:,:,1) + 1/3*MyImage(:,:,2) + 1/3*MyImage(:,:,3);
Gray = uint8(Gray);
Gray2 = rgb2gray(uint8(MyImage));
size(Gray)
figure; imshow(Gray);
figure; imshow(Gray2);

Gray = double (Gray);
Gray2 = double (Gray2);
max(max(Gray2 - Gray))

Gray3 = 0.2989 * MyImage(:,:,1) + 0.5870 * MyImage(:,:,2) + 0.1140 * MyImage(:,:,3);
max(max(Gray2 - Gray3))
figure; imshow(uint8(Gray3));
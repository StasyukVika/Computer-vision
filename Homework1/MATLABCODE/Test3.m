close all;
MyImage = imread('N1.png');
Gray = rgb2gray(MyImage);
figure; imshow(Gray);
int = zeros(1,256);
Gray = Gray(:);
for i=0:255
    int(i+1) = sum(Gray == i);
end
figure; bar(int);
axis([0 255 min(int) max(int)])
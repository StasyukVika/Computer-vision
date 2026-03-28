Im1 = imread('N1.jpg');
Gray = rgb2gray(Im1);
imshow(Gray);

WM = imread('WM.png');
Gray = rgb2gray(WM);
BWM = Gray>127;
imshow(BWM)
whos BWM
surf(double(BWM))
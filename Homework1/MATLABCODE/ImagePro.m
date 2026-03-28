FirstIm = imread('Im1.jpg');
SecondIm = imread('Im2.jpg');
figure; imshow(FirstIm)
figure; imshow(SecondIm)
TrirdIm = 255-SecondIm;
figure; imshow(TrirdIm)

size(FirstIm)

Im1 = imread('N1.jpg');
Im2 = imread('N2.jpg');
figure;
subplot(1,2,1); imshow(Im1);
subplot(1,2,2); imshow(Im2);

Im1 = double(Im1);
Im2 = double(Im2);
figure;
% for a = 0:0.01:1    
%     Im_rez = a*Im1 + (1-a)*Im2;
%     Im_rez = uint8(Im_rez);
%     imshow(Im_rez);
%     pause(1e-5);
% end

[M,N,C] = size(Im1);
Im_rez2 = zeros(M,N,C);
a = 0.5;
tic;
for i=1:M
    for j=1:N
        for k=1:C
            Im_rez2(i,j,k) = a*Im1(i,j,k) + (1-a)*Im2(i,j,k);
        end
    end
end
toc;
Im_rez2 = uint8(Im_rez2);
imshow(Im_rez2);
imwrite(Im_rez2,'rez.jpg','jpg');


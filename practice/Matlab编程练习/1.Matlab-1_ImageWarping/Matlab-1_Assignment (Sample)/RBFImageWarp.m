function [im2, q0] = RBFImageWarp(im, psrc, pdst)

% input: im, psrc, pdst

%% map
% f(x,y) = (x,y) + sum_i( ai*exp( -d^2( [x1 y1]-[pxi pyi] )/delta^2 ) );

% parameter for Gaussian basis 
delta2 = 1000;

%% construct matrix for linear system
npts = size(psrc, 1);
A = zeros(npts);
for i=1:npts
    A(:,i) = exp( -sum( (psrc(i,:) - psrc).^2, 2 )/delta2 );
end

%% solve for warp coefficients
coef = A\(pdst-psrc);


%% mapped position for each source pixel
[h, w, dim] = size(im);
[xpix, ypix] = meshgrid(1:w, 1:h);

B = zeros(h*w, npts);
for i=1:npts
    B(:,i) = exp( -sum( (psrc(i,:) - [xpix(:) ypix(:)]).^2, 2 )/delta2 );
end

q0 = B*coef + [xpix(:) ypix(:)];

%% assign result image
q = ceil(q0);
pixflag = all(q>0,2) & (q(:,1)<=w) & (q(:,2)<=h);
mapPixIdx = sub2ind([h w], q(pixflag,2), q(pixflag,1));

im = reshape(im, [h*w 3]);

im2 = ones(h*w, 3, 'uint8')*255;
im2(mapPixIdx, :) = im(pixflag,:);
im2 = reshape(im2, [h w 3]);

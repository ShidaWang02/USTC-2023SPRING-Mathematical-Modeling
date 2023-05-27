function im2 = RBFImageWarp(im, psrc, pdst)

% input: im, psrc, pdst


%% basic image manipulations
% get image (matrix) size
[h, w, dim] = size(im);

im2 = im;

%% use loop to negate image
for i=1:h
    for j=1:w
        for k=1:dim
            im2(i, j, k) = 255 - im(i, j, k);
        end
    end
end


%% TODO: compute warpped image
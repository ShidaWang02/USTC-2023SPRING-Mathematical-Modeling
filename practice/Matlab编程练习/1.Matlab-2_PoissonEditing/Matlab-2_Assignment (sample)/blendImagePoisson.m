function imret = blendImagePoisson(im1, im2, roi, targetPosition)

% input: im1 (background), im2 (foreground), roi (in im2), targetPosition (in im1)

[hdst, wdst, dim] = size(im1);
   
%% preprocessing
persistent roi0 gCopy u Mdst edst
if isempty(roi0) || numel(roi0)~=numel(roi) || norm(roi0-roi,'fro') > 1e-6
    %% construct gradient operator for im1
    [Mdst, edst] = constructImageGradMatrix(wdst, hdst);

    %% construct gradient operator for im2
    [hsrc, wsrc, dim] = size(im2);
    [Msrc, esrc] = constructImageGradMatrix(wsrc, hsrc);
    [ey0, ex0] = ind2sub([hsrc wsrc], esrc(:,1));

    % find edges that are inside the copying region
    eflagsrc = reshape(inpolygon( ex0, ey0, roi(:,1), roi(:,2) ), [], 1);
    gCopy = Msrc(eflagsrc,:)*double( reshape(im2, [], dim) );
    
    %%
    [ey1, ex1] = ind2sub([hdst wdst], edst(:,1));
    eflagdst = reshape(inpolygon( ex1, ey1, targetPosition(:,1), targetPosition(:,2) ), [], 1);
    vflag = false(wdst*hdst,1);
    vflag( edst(eflagdst,1) ) = true;
    A = Mdst(eflagdst, :);
    u = chol( A(:, vflag)'*A(:, vflag) );

    roi0 = roi;
end


%% update A for new targetPosition
[ey1, ex1] = ind2sub([hdst wdst], edst(:,1));
eflagdst = reshape(inpolygon( ex1, ey1, targetPosition(:,1), targetPosition(:,2) ), [], 1);
vflag = false(wdst*hdst,1);
vflag( edst(eflagdst,1) ) = true;
A = Mdst(eflagdst, :);


%%
% convert to double for linear system solve
im1 = double(reshape(im1, [], dim));
% min |A*im1|^2
im1(vflag, :) = u\(u'\(A(:, vflag)'*(gCopy - A(:,~vflag)*im1(~vflag, :))));
imret = reshape( uint8(im1), hdst, wdst, dim);


function [M, e] = constructImageGradMatrix(w, h)

[xpix, ypix] = meshgrid(1:w, 1:h);

ex = [ reshape( sub2ind([h, w], ypix(:,1:end-1), xpix(:, 1:end-1)), [], 1 ) ...
       reshape( sub2ind([h, w], ypix(:,2:end),   xpix(:, 2:end)),   [], 1 ) ];

ey = [ reshape( sub2ind([h, w], ypix(1:end-1, :),xpix(1:end-1, :)), [], 1 ) ...
       reshape( sub2ind([h, w], ypix(2:end, :),  xpix(2:end, :)),   [], 1 ) ];
   
ex = [ex; ex(:, [2 1])];
ey = [ey; ey(:, [2 1])];

nex = size(ex,1);
pix2gradx = sparse( repmat( (1:nex)', 1, 2 ), ex, repmat([1 -1], nex, 1), nex, w*h );

ney = size(ey,1);
pix2grady = sparse( repmat( (1:ney)', 1, 2 ), ey, repmat([1 -1], ney, 1), ney, w*h );

M = [pix2gradx; pix2grady];
e = [ex; ey];

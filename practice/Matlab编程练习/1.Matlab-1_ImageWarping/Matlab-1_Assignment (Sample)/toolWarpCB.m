function toolWarpCB(varargin)

hlines = evalin('base', 'hToolPoint.UserData');
hlines = hlines( isvalid(hlines) );

im = evalin('base', 'im');
himg = evalin('base', 'himg');
hsurf = evalin('base', 'hsurf');

p2p = zeros(numel(hlines)*2,2); 
for i=1:numel(hlines)
    p2p(i*2+(-1:0),:) = hlines(i).getPosition();
end

[im2, q] = RBFImageWarp(im, p2p(1:2:end,:), p2p(2:2:end,:));
set(himg, 'CData', im2);

[h, w, ~] = size(im);
set(hsurf, 'XData', reshape(q(:,1), h, w), 'YData', reshape(q(:,2), h, w));
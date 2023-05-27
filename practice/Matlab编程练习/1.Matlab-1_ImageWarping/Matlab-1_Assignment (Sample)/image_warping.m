%% read image
im = imread('warp_test.png');

%% draw 2 copies of the image
figure('Units', 'pixel', 'Position', [100,100,1000,700], 'toolbar', 'none');
subplot(131); imshow(im); title({'Source image'});
subplot(132); himg = imshow(im*0); title({'Warpped Image'});
[h, w, d] = size(im);
[xpix, ypix] = meshgrid(1:w, 1:h);
subplot(133); hsurf = surface('LineStyle','none', 'FaceColor','texturemap', 'Visible', 'on', 'CData', im, ...
                              'XData', xpix, 'YData', ypix, 'ZData', xpix*0); axis equal; axis off;
set(gca,'ydir','reverse'); axis([0 h 0 w]+0.5); title({'Warpped Image ver 2'});


hToolPoint = uipushtool('CData', reshape(repmat([1 0 0], 100, 1), [10 10 3]), 'TooltipString', 'add point constraints to the map', ...
                        'ClickedCallback', @toolPositionCB, 'UserData', []);
hToolWarp = uipushtool('CData', reshape(repmat([0 0 1], 100, 1), [10 10 3]), 'TooltipString', 'compute warped image', ...
                       'ClickedCallback', @toolWarpCB);

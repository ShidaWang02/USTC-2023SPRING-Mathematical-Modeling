im1 = imread('../TestImages/NewBackGround.png');
im2 = imread('../TestImages/BearInWater.png');
% im2 = imread('../TestImages/GirlInWater.png');

%% draw 2 copies of the image
figure('Units', 'pixel', 'Position', [100,100,1000,700], 'toolbar', 'none');
subplot(121); imshow(im2); title({'Foreground', 'press red tool button to mark polygon as copying region'});
subplot(122); himg = imshow(im1); title({'Background', 'press blue tool button to compute blended image'});

hpolys = [];
hToolMark = uipushtool('CData', reshape(repmat([1 0 0], 100, 1), [10 10 3]), 'TooltipString', 'define copying region on the foreground image', 'ClickedCallback', @toolMarkCB);
hToolWarp = uipushtool('CData', reshape(repmat([0 0 1], 100, 1), [10 10 3]), 'TooltipString', 'compute blended image', 'ClickedCallback', @toolPasteCB);

%% TODO: implement function: blendImagePoisson
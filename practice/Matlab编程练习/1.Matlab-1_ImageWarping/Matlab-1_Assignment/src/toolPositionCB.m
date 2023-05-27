function toolPositionCB(h, varargin)

set(h, 'Enable', 'off');

subplot(121);
set(h, 'Enable', 'on', 'UserData', [h.UserData, imline]);

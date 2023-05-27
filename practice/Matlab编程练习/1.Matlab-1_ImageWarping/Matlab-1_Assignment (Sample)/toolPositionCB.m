function toolPositionCB(h, varargin)

set(h, 'Enable', 'off');

subplot(131);
hImLines = [h.UserData, imline];
set(h, 'Enable', 'on', 'UserData', hImLines);

toolWarpCB;
hImLines(end).addNewPositionCallback(@toolWarpCB);


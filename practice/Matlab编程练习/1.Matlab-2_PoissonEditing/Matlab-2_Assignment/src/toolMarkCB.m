function toolMarkCB(h, varargin)

evalin('base', 'delete(hpolys);');

set(h, 'Enable', 'off');

hp1 = impoly(subplot(121));
hp1.setVerticesDraggable(false);

hp2 = impoly(subplot(122), hp1.getPosition);
hp2.setVerticesDraggable(false);

assignin('base', 'hpolys', [hp1; hp2]);

set(h, 'Enable', 'on');
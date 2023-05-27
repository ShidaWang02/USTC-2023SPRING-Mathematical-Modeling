[x, t] = readObj('../meshes/Cat_head.obj');

%% draw 2 copies of the image
figure; set(gcf, 'Units', 'normalized', 'Position', [0.05,0.05,.8,.8]);
subplot(121); trimesh(t, x(:,1), x(:,2), x(:,3), 'edgecolor', 'k'); axis off; axis equal; title('input');
subplot(122); h = trimesh(t, x(:,1), x(:,2), x(:,3), 'edgecolor', 'k'); axis off; axis equal; title('output');

%% TODO: find boundary and interior vertices

%% TODO: compute Laplacian
L = laplacian(x, t);

%% TODO: compute minimal surface using LOCAL approach

%% TODO: compute minimal surface using GLOBAL approach

%% draw mesh in minimal surface iterations
set(h, 'Vertices', x);
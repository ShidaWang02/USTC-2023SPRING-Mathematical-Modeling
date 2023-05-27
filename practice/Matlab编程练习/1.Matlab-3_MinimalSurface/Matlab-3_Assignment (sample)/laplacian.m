function L = laplacian(x, t)

% compute cotanget Laplacan of mesh (x, t)

frownorm2 = @(M) sum(M.^2, 2);
el2 = frownorm2( x(t(:, [2 3 1]), :) - x(t(:, [3 1 2]), :) );
el2 = reshape( el2, [], 3 );
coss = el2*[-1 1 1; 1 -1 1; 1 1 -1]*0.5 ./ sqrt(el2(:, [2 3 1]).*el2(:, [3 1 2]));

nv = size(x, 1);
L = sparse( t(:,[2 3 1]), t(:,[3 1 2]), cot(acos(coss)), nv, nv );
L = L + L';
L = -spdiags(-sum(L,2), 0, L);

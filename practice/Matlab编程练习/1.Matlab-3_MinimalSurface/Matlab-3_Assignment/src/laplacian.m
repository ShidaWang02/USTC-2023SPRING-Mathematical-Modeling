function L = laplacian(x, t)

% compute cotanget Laplacan of mesh (x, t)

nv = size(x, 1);
nf = size(t, 1);
L = sparse(nv, nv);


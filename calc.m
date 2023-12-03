function getBP(f_m)

N = 32;
f_s = 4000;

% Coefficients...
b0 = 1.0;

k = floor(0.5 + (N * f_m / f_s));
w = 2 * pi * k / N;
a0 = -2 * cos(w);

a1 = 1.0;

fvtool([b0], [1, a0, a1], "Fs", f_s);
disp(a0);

end
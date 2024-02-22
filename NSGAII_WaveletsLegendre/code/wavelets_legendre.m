function C = wavelets_legendre(F1, F2, M, k, s)
    t = linspace(0, 1, (2^(k-1)) * (M));
    n=2^(k-1)*(M-1);
    C = sym('c',[1 n]);
    S = zeros(2^(k-1)*M, 1);
    
    for i = 1:(2^(k-1)*M)
        xi = cos((2*i + 1)*pi/(2^k)*M);
        ci = 0;
        for j = 1:s
            tauj = j;
            ci = ci + F1((xi/2) *(tauj + 1), dot(C, wavelet(M, k, (xi/2) *(tauj + 1))));
        end
        disp(ci)
    end

end
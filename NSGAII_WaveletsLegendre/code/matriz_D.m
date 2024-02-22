function D = matriz_D(M,k,i)
    D = {zeros(2^k*(M+1),2^k*(M+1))};
    for i = 1:2^k*(M+1)
        D{i,i} = matriz_F(M,k)^i;
    end
end
function F = matriz_F(M,k)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
F = zeros(M+1,M+1);
    for i = 1:M+1
        for j = 1:M+1
            if j<i
                if mod(i,2)>0
                    if mod(j,2)==0
                    F(i,j) = sqrt(2*i-1)*sqrt(2*j-1);
                    end
                else
                    if mod(j,2)>0
                    F(i,j) = sqrt(2*i-1)*sqrt(2*j-1);
                    end
                end
            end
        end
    end
F = 2^(k+1)*F;
end

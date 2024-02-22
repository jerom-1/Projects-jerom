function f = initialize_variables(N, M, V, min_range, max_range)
%% La siguiente función está adaptada para la solución del parcial II del
% curso Optimización II
%% function f = initialize_variables(N, M, V, min_tange, max_range) 
% This function initializes the chromosomes. Each chromosome has the
% Esta fubción inicializa los Cromosomas. Cada cromosoma debe tener los
% siguiente en esta etapa:
%       * Variables de decisión
%       * Valores de la función Objetivo
% donde,
% N - Tamaño de la población        (Individuos)
% M - Número de funciones objetivo  (Dimensión del espacio de puntos)
% V - Número de variables de decisión  (dimensión de los vectores)
% min_range - Vector numérico de valores con el valor mínimo
% (en la población) que llega a tener cada variable de decisión para cada 
% Función objetivo.
% max_range - Vector numérico de valores con el valor máximo
% (en la población) que llega a tener cada variable de decisión para cada 
% Función objetivo..

%  Copyright (c) 2009, Aravind Seshadri
%  All rights reserved.
%
%  Redistribution and use in source and binary forms, with or without 
%  modification, are permitted provided that the following conditions are 
%  met:
%
%     * Redistributions of source code must retain the above copyright 
%       notice, this list of conditions and the following disclaimer.
%     * Redistributions in binary form must reproduce the above copyright 
%       notice, this list of conditions and the following disclaimer in 
%       the documentation and/or other materials provided with the distribution
%      
%  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
%  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
%  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
%  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
%  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
%  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
%  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
%  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
%  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
%  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
%  POSSIBILITY OF SUCH DAMAGE.

min = min_range;
max = max_range;

% K is the total number of array elements. For ease of computation, decision
% variables and objective functions are concatenated to form a single
% array. For crossover and mutation only the decision variables are used
% while for selection, only the objective variable are utilized.
%Se establece un súper arreglo (x,f(x)) tal que se junten las variables de
%decisión y su respectiva imagen en la función objetivo

K = M + V;

%% Initialize each chromosome
% For each chromosome perform the following (N is the population size)
for i = 1 : N
    % Initialize the decision variables based on the minimum and maximum
    % possible values. V is the number of decision variable. A random
    % number is picked between the minimum and maximum possible values for
    % the each decision variable.
    for j = 1 : V
        f(i,j) = min(j) + (max(j) - min(j))*rand(1);
    end
    % For ease of computation and handling data the chromosome also has the
    % vlaue of the objective function concatenated at the end. The elements
    % V + 1 to K has the objective function valued. 
    % The function evaluate_objective takes one chromosome at a time,
    % infact only the decision variables are passed to the function along
    % with information about the number of objective functions which are
    % processed and returns the value for the objective functions. These
    % values are now stored at the end of the chromosome itself.
    % v+1 -> k desde la columna v+1 hasta la k (para dejar la imagen del cr
    % cromosoma).
    f(i,V + 1: K) = evaluate_objective(f(i,:), M, V);
end

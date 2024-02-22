function ultgen = nsga_2(pop,gen)

%% function nsga_2(pop,gen)
% pop - Tamaño de la población
% gen - Número total de generaciones
%
% Original algorithm NSGA-II was developed by researchers in Kanpur Genetic
% Algorithm Labarotary and kindly visit their website for more information
% http://www.iitk.ac.in/kangal/


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

%% Simple error checking
% Number of Arguments
% Check for the number of arguments. The two input arguments are necessary
% to run this function.
if nargin < 2
    error('Insuficientes argumentos entregados');
end
% Both the input arguments need to of integer data type
if isnumeric(pop) == 0 || isnumeric(gen) == 0
    error('Los argumentos deben ser números enteros');
end
% Minimum population size has to be 20 individuals
if pop < 20
    error('20 es el tamaño mínimo de población inicial');
end
if gen < 5
    error('5 son las generaciones mínimas');
end

pop = round(pop);
gen = round(gen);

%% Funcion Objetivo
[M, V, min_range, max_range] = objective_description_function();

%% Initialize the population
% La población inicial se inicializa con valores aleatorios dentro del
% rango especificado por el usuario.
chromosome = initialize_variables(pop, M, V, min_range, max_range);


%% Ordenar la población Inicial
% Se retornan 2 columnas (atributos) por cada individuo de la población.
% Los atributos son el p_rank y la distacia de hacinamiento.
chromosome = non_domination_sort_mod(chromosome, M, V);

%% Iniciar proceso de evolución
% Para cada generación
% * Escoger padres con el torneo binario
% * Operar en los individuos con cruces y mutaciones
% * Ordenar y escoger a la siguiente generación
% * Reemplazar individuos para mantener el tamaño de la población.

for i = 1 : gen
    % Select the parents
    % Parents are selected for reproduction to generate offspring. The
    % original NSGA-II uses a binary tournament selection based on the
    % crowded-comparision operator. The arguments are 
    % pool - tamaño del grupo de cruce.
    % tour - emparejamiento 1 a 1 en el torneo binario.
    pool = round(pop/2);
    tour = 2;
    % Selection process
    % A binary tournament selection is employed in NSGA-II. In a binary
    % tournament selection process two individuals are selected at random
    % and their fitness is compared. The individual with better fitness is
    % selcted as a parent. Tournament selection is carried out until the
    % pool size is filled. Basically a pool size is the number of parents
    % to be selected. The input arguments to the function
    % tournament_selection are chromosome, pool, tour.
    parent_chromosome = tournament_selection(chromosome, pool, tour);

    % Perfrom crossover and Mutation operator
    % The original NSGA-II algorithm uses Simulated Binary Crossover (SBX) and
    % Polynomial  mutation. Crossover probability pc = 0.9 and mutation
    % probability is pm = 1/n, where n is the number of decision variables.
    % Both real-coded GA and binary-coded GA are implemented in the original
    % algorithm, while in this program only the real-coded GA is considered.
    % The distribution indices for crossover and mutation operators as mu = 20
    % and mum = 20 respectively.
    mu = 18;
    mum = 20;
    offspring_chromosome = ...
        genetic_operator(parent_chromosome, ...
        M, V, mu, mum, min_range, max_range);

    % Intermediate population
    % Intermediate population is the combined population of parents and
    % offsprings of the current generation. The population size is two
    % times the initial population.
    
    [main_pop,temp] = size(chromosome);
    [offspring_pop,temp] = size(offspring_chromosome);
    % temp is a dummy variable. Solo para guardar las dimensiones columna
    clear temp
    % intermediate_chromosome is a concatenation of current population and
    % the offspring population.
    intermediate_chromosome(1:main_pop,:) = chromosome;
    intermediate_chromosome(main_pop + 1 : main_pop + offspring_pop,1 : M+V) = ...
        offspring_chromosome;

    % Non-domination-sort of intermediate population
    % The intermediate population is sorted again based on non-domination sort
    % before the replacement operator is performed on the intermediate
    % population.
    intermediate_chromosome = ...
        non_domination_sort_mod(intermediate_chromosome, M, V);
    % Perform Selection
    % Once the intermediate population is sorted only the best solution is
    % selected based on it rank and crowding distance. Each front is filled in
    % ascending order until the addition of population size is reached. The
    % last front is included in the population based on the individuals with
    % least crowding distance
    chromosome = replace_chromosome(intermediate_chromosome, M, V, pop);
    if ~mod(i,25)
        clc
        fprintf('%d generaciones completas\n',i);
        plot3(chromosome(:,V + 1),chromosome(:,V + 2),chromosome(:,V + 3),...
        'ro')
    end
end
ultgen = chromosome(:,[1:V V+8]);
if M == 2
    plot(chromosome(:,V + 1),chromosome(:,V + 2),'*');
elseif M ==3
    %Construcción de malla
    %[l,m]=meshgrid(-5:0.001:5);
    ultgen = chromosome;
    %f123 = [chromosome(:,V + 1),chromosome(:,V + 2),chromosome(:,V + 3)];
    %contour3([chromosome(:,V + 1),chromosome(:,V + 2),chromosome(:,V + 3)]);
    plot3(chromosome(:,V + 1),chromosome(:,V + 2),chromosome(:,V + 3),...
        'ro')
    xlabel('f_1')
    ylabel('f_2')
    zlabel('f_3');
    % plotmatrix(f123)
    % title(BigAx,'Comparación entre funciones')
end
    

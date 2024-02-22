syms A00 A01 t
assume(t,'real');
assume(A00,'real');
assume(A01,'real');

phi00 = @(t) 1;
phi01 = @(t) sqrt(3)*(2*t-1);
A = [A00
     A01];
phit = @(t) [phi00(t)
    phi01(t)];
y = @(t) A'*phit(t);
D = [0 0
    2*sqrt(3) 0];
yp = @(t) A'*D*phit(t);

e421 = @(t) yp(t)+t*y(t-t^2)+t*y(t)^2-1-t^2;

eq1 = vpa(y(0)==0); 
eq2 = vpa(e421(0.211)==0);
sol = solve([eq1,eq2],[A00,A01]);

B = [sol.A00(1)
    sol.A01(1)];
y2 = @(t) B'*phit(t);

B2 = [0.5891
    0.3514];

y3 = @(t) B2'*phit(t);

t_values = linspace(0, 1, 100);  % Valores de t en el rango de interés
y_values = subs(y2, {t}, t_values); % Evaluación de la expresión de y en los valores de t
y_genval = subs(y2, {t}, t_values);
plot(t_values, y_values);
xlabel('t');
ylabel('y');
title('Gráfico de la expresión de y');
hold on
plot(t_values, y_genval);
hold off

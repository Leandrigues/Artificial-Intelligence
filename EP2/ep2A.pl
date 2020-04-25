%%%%% Insira aqui os seus predicados.
%%%%% Use quantos predicados auxiliares julgar necess�rio

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

lista_para_conjunto(Xs, Cs) :- ex1Helper(Xs, [], Cs).

ex1Helper([], Cs, Cs).

ex1Helper([X | Xs], H, Cs) :-
    \+member(X, H), append(H, [X], K), ex1Helper(Xs, K, Cs).

ex1Helper([X | Xs], H, Cs) :-
    member(X, H), ex1Helper(Xs, H, Cs).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

mesmo_conjunto(Xs, Ys) :-
    list_same_length(Xs, Ys),  
    ex2Helper(Xs,   Ys).

ex2Helper([], Ys).

list_same_length([], []).
list_same_length([_|Xs], [_|Ys]) :-
    list_same_length(Xs, Ys).


ex2Helper([X | Xs], Ys) :-
    member(X, Ys),
    % contido(Ys, Xs),
    ex2Helper(Xs, Ys).

contido([A | As], Bs) :-
    member(A, Bs),
    contido(As, Bs).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

uniao_conjunto(Cs, Ds, Es) :-
    ex3Helper(Cs, Ds, [], Es).

ex3Helper([], [], Result, Result).

ex3Helper([C | Cs], Ds, Es, Result) :-
    \+member(C, Es), append(Es, [C], F), ex3Helper(Cs, Ds, F, Result);
    member(C, Es), ex3Helper(Cs, Ds, Es, Result).

ex3Helper([], [D | Ds], Es, Result) :-
    \+member(D, Es), append(Es, [D], F), ex3Helper([], Ds, F, Result);
    member(D, Es), ex3Helper([], Ds, Es, Result).
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

inter_conjunto(Cs, Ds, Es) :-
    exHelper4(Cs, Ds, [], Es).

exHelper4([], _, Result, Result).

exHelper4([C | Cs], Ds, Es, Result) :-
    member(C, Ds), append(Es, [C], F), exHelper4(Cs, Ds, F, Result);
    \+member(C, Ds), exHelper4(Cs, Ds, Es, Result).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
diferenca_conjunto(Cs, Ds, Es) :-
    ex5Helper(Cs, Ds, [], Es).

ex5Helper([], _, Result, Result).

ex5Helper([C | Cs], Ds, Es, Result) :-
    \+member(C, Ds), append([C], Es, F), ex5Helper(Cs, Ds, F, Result);
    member(C, Ds), ex5Helper(Cs, Ds, Es, Result).




%%%%%%%% Fim dos predicados adicionados
%%%%%%%% Os testes come�am aqui.
%%%%%%%% Para executar os testes, use a consulta:   ?- run_tests.

%%%%%%%% Mais informacoes sobre testes podem ser encontradas em:
%%%%%%%%    https://www.swi-prolog.org/pldoc/package/plunit.html

:- begin_tests(conjuntos).
test(lista_para_conjunto, all(Xs=[[1,a,3,4]]) ) :-
    lista_para_conjunto([1,a,3,3,a,1,4], Xs).
test(lista_para_conjunto2,fail) :-
    lista_para_conjunto([1,a,3,3,a,1,4], [a,1,3,4]).

test(mesmo_conjunto, set(Xs=[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    mesmo_conjunto([1,a,3], Xs).

test(uniao_conjunto2,fail) :-
    mesmo_conjunto([1,a,3,4], [1,3,4]).

test(uniao_conjunto, set(Ys==[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    uniao_conjunto([1,a], [a,3], Xs),
    mesmo_conjunto(Xs,Ys).
test(uniao_conjunto2,fail) :-
    uniao_conjunto([1,a,3,4], [1,2,3,4], [1,1,a,2,3,3,4,4]).

test(inter_conjunto, all(Xs==[[1,3,4]])) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], Xs).
test(inter_conjunto2,fail) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], [1,1,3,3,4,4]).

test(diferenca_conjunto, all(Xs==[[2]])) :-
    diferenca_conjunto([1,2,3], [3,a,1], Xs).
test(diferenca_conjunto2,fail) :-
    diferenca_conjunto([1,3,4], [1,2,3,4], [_|_]).

:- end_tests(conjuntos).

"""Verificação exaustiva, em grafos pequenos, de resultados da tese.

1. Teorema 4.1: G □ H (G, H conexos não triviais) tem uma 2-atribuição de papéis;
   conferimos a construção do teorema.
2. Teorema 5.11: o prisma complementar de G tem uma 2-atribuição de papéis se e somente
   se G não é P3 nem o complemento de P3. Conferido para todos os grafos rotulados com
   2 a 5 vértices.
3. Lista, a título de observação, os grafos (até isomorfismo) com n <= 5 cujo prisma
   complementar NÃO tem 3-atribuição de papéis.
"""
from itertools import combinations, permutations

from roles import (cartesian_product, complement, complementary_prism,
                   find_role_assignment, graph_from_edges, is_connected,
                   is_role_assignment, two_role_cartesian)


def all_graphs(n):
    pairs = list(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        yield graph_from_edges(n, [e for i, e in enumerate(pairs) if mask >> i & 1])


def canon(adj):
    n = len(adj)
    best = None
    for perm in permutations(range(n)):
        edges = tuple(sorted(tuple(sorted((perm[u], perm[v])))
                             for u in adj for v in adj[u] if u < v))
        best = edges if best is None or edges < best else best
    return best


def is_p3(adj):
    return len(adj) == 3 and sorted(len(a) for a in adj.values()) == [1, 1, 2]


def check_cartesian():
    graphs = [g for n in (2, 3, 4) for g in all_graphs(n) if is_connected(g)]
    ok = 0
    for g in graphs:
        for h in graphs:
            prod = cartesian_product(g, h)
            p = two_role_cartesian(g, h)
            assert is_role_assignment(prod, p, 2), (g, h)
            ok += 1
    print(f"Teorema 4.1: construção válida em {ok} produtos G□H (G, H conexos, 2 a 4 vértices)")


def check_2_assignment():
    for n in range(2, 6):
        total = bad = 0
        for g in all_graphs(n):
            has = find_role_assignment(complementary_prism(g), 2) is not None
            exception = is_p3(g) or is_p3(complement(g))
            assert has == (not exception), (n, g)
            total += 1
            bad += exception
        print(f"Teorema 5.11, n={n}: confere em {total} grafos ({bad} exceções P3/complemento)")


def list_without_3_assignment():
    for n in range(2, 6):
        seen = {}
        for g in all_graphs(n):
            c = canon(g)
            if c in seen:
                continue
            seen[c] = find_role_assignment(complementary_prism(g), 3) is None
        no = [c for c, v in seen.items() if v]
        print(f"n={n}: {len(no)} de {len(seen)} grafos (até isomorfismo) sem 3-atribuição")
        for c in no:
            print("   arestas:", list(c))


if __name__ == "__main__":
    check_cartesian()
    check_2_assignment()
    list_without_3_assignment()
